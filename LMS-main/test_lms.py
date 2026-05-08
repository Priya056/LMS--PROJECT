#!/usr/bin/env python3
"""
Direct check50 runner for Windows
Tests the LMS without requiring the check50 command-line interface
"""

import sys
import os
import requests
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

def get_unique_email():
    """Generate unique email"""
    return f"test{int(time.time()*1000000)}@example.com"

def print_test(name, passed, message=""):
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {name}")
    if message:
        print(f"  {message}")

def test_health_endpoint():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)
        passed = response.status_code == 200 and response.json().get("status") == "ok"
        print_test("Health endpoint returns 200", passed)
        return passed
    except Exception as e:
        print_test("Health endpoint returns 200", False, str(e))
        return False

def test_register():
    """Test user registration"""
    try:
        user_data = {
            "email": get_unique_email(),
            "password": "testpass123",
            "name": "Test User"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user_data,
            timeout=TIMEOUT
        )
        passed = response.status_code == 200 and "access_token" in response.json()
        print_test("User registration works", passed)
        return passed, response.json() if passed else None, user_data
    except Exception as e:
        print_test("User registration works", False, str(e))
        return False, None, None

def test_login():
    """Test user login"""
    try:
        user_data = {
            "email": get_unique_email(),
            "password": "testpass123",
            "name": "Test User"
        }
        # Register first
        reg_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user_data,
            timeout=TIMEOUT
        )
        if reg_response.status_code != 200:
            print_test("User login works", False, "Registration failed")
            return False, None
        
        # Then login
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": user_data["email"], "password": user_data["password"]},
            timeout=TIMEOUT
        )
        passed = response.status_code == 200 and "access_token" in response.json()
        print_test("User login works", passed)
        return passed, response.json() if passed else None
    except Exception as e:
        print_test("User login works", False, str(e))
        return False, None

def test_protected_without_auth():
    """Test that protected endpoints require auth"""
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", timeout=TIMEOUT)
        passed = response.status_code == 401
        print_test("Protected endpoints require authentication", passed, f"Expected 401, got {response.status_code}")
        return passed
    except Exception as e:
        print_test("Protected endpoints require authentication", False, str(e))
        return False

def test_protected_with_auth():
    """Test protected endpoints with auth"""
    try:
        # Register user
        user_email = get_unique_email()
        reg_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"email": user_email, "password": "test123456", "name": "Test User 2"},
            timeout=TIMEOUT
        )
        if reg_response.status_code != 200:
            print_test("Protected endpoints work with authentication", False, "Registration failed")
            return False
        
        token = reg_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers, timeout=TIMEOUT)
        passed = response.status_code == 200
        print_test("Protected endpoints work with authentication", passed)
        return passed
    except Exception as e:
        print_test("Protected endpoints work with authentication", False, str(e))
        return False

def test_courses_endpoint():
    """Test courses endpoint"""
    try:
        # Register user
        user_email = get_unique_email()
        reg_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"email": user_email, "password": "test123456", "name": "Test User 3"},
            timeout=TIMEOUT
        )
        if reg_response.status_code != 200:
            print_test("Courses endpoint returns courses", False, "Registration failed")
            return False
        
        token = reg_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(f"{BASE_URL}/api/courses", headers=headers, timeout=TIMEOUT)
        passed = response.status_code == 200 and isinstance(response.json(), list) and len(response.json()) > 0
        print_test("Courses endpoint returns courses", passed, f"Found {len(response.json()) if passed else 0} courses")
        return passed
    except Exception as e:
        print_test("Courses endpoint returns courses", False, str(e))
        return False

def test_invalid_credentials():
    """Test that invalid credentials are rejected"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "wrongpassword"},
            timeout=TIMEOUT
        )
        passed = response.status_code == 401
        print_test("Invalid credentials rejected", passed)
        return passed
    except Exception as e:
        print_test("Invalid credentials rejected", False, str(e))
        return False

def test_duplicate_email():
    """Test that duplicate email registration is rejected"""
    try:
        user_email = get_unique_email()
        # Register first user
        first_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"email": user_email, "password": "test123456", "name": "Test User 4"},
            timeout=TIMEOUT
        )
        if first_response.status_code != 200:
            print_test("Duplicate email rejected", False, "First registration failed")
            return False
        
        # Try to register same email
        second_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"email": user_email, "password": "test123456", "name": "Test User 4"},
            timeout=TIMEOUT
        )
        passed = second_response.status_code == 400
        print_test("Duplicate email rejected", passed)
        return passed
    except Exception as e:
        print_test("Duplicate email rejected", False, str(e))
        return False

def main():
    print("=" * 60)
    print("LMS Check50 Tests")
    print("=" * 60)
    print()
    
    # Check if server is running
    print("Checking if server is running...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print("✓ Server is running\n")
    except Exception as e:
        print(f"✗ Server is not running: {e}")
        print("Please start the backend server first:")
        print("  cd backend")
        print("  python -m uvicorn app.main:app --host 127.0.0.1 --port 8000")
        sys.exit(1)
    
    # Run tests
    results = []
    results.append(test_health_endpoint())
    results.append(test_register()[0])
    results.append(test_login()[0])
    results.append(test_protected_without_auth())
    results.append(test_protected_with_auth())
    results.append(test_courses_endpoint())
    results.append(test_invalid_credentials())
    results.append(test_duplicate_email())
    
    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
