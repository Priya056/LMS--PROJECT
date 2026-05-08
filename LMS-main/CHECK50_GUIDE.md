# Check50 Setup Guide for Fraylon Academy LMS

## Overview

This project now includes automated check50 checks to verify the functionality of the Fraylon Academy LMS. These checks test:

- ✓ App starts without errors
- ✓ Health endpoint returns correct status
- ✓ Database initialization
- ✓ User registration functionality
- ✓ User login functionality  
- ✓ Protected endpoints require authentication
- ✓ Protected endpoints work with valid authentication
- ✓ Courses endpoint returns course data
- ✓ Invalid credentials are rejected
- ✓ Duplicate email registration is rejected

## Files Created

### 1. Check Module (`checks/check50.py`)
Located at: `checks/check50.py`

Contains all the check50 test functions using the check50 API. Each check includes:
- Automatic app startup/shutdown management
- Comprehensive error handling
- Detailed logging for debugging
- Tests for critical API endpoints

**Key Features:**
- Uses context managers to safely manage FastAPI server lifecycle
- Generates unique test data to avoid conflicts
- Comprehensive endpoint coverage
- Clear pass/fail messages

### 2. Configuration File (`.check50.yaml`)
Located at: `.check50.yaml`

Defines:
- List of all checks and their slugs
- Dependencies required (FastAPI, Uvicorn, SQLAlchemy, etc.)
- Entry point for check50 (`checks.check50`)

### 3. Test Runner (`test_lms.py`)
Located at: `test_lms.py`

A Windows-friendly test runner that doesn't require the full check50 CLI infrastructure. It:
- Tests all critical endpoints
- Generates detailed test reports
- Returns proper exit codes for CI/CD integration
- Uses unique email addresses to avoid database conflicts

### 4. Updated Requirements
Updated: `backend/requirements.txt`

Added:
- `requests==2.31.0` - For HTTP testing in check50 tests

## Running the Checks

### Option 1: Using the Test Runner (Recommended for Windows)

```bash
# 1. Start the backend server
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# 2. In a new terminal, run the tests
python test_lms.py
```

**Expected Output:**
```
============================================================
LMS Check50 Tests
============================================================

Checking if server is running...
✓ Server is running

✓ PASS: Health endpoint returns 200
✓ PASS: User registration works
✓ PASS: User login works
✓ PASS: Protected endpoints require authentication
✓ PASS: Protected endpoints work with authentication
✓ PASS: Courses endpoint returns courses
  Found 2 courses
✓ PASS: Invalid credentials rejected
✓ PASS: Duplicate email rejected

============================================================
Results: 8/8 tests passed
============================================================
```

### Option 2: Using check50 CLI (Linux/macOS/WSL)

If you're on Unix-like systems, you can use the native check50 command:

```bash
# Install check50 if not already installed
pip install check50

# Run checks from GitHub (once pushed)
check50 Priya056/LMS--PROJECT/main
```

Note: check50 requires Unix-based systems (Linux, macOS, WSL). On native Windows, the Unix module `termios` is not available.

## Test Details

### Health Endpoint
- **Endpoint:** `GET /api/health`
- **Expected:** Status 200 with `{"status": "ok", "service": "fraylon-academy-lms"}`
- **Tests:** Server is running and responding

### User Registration
- **Endpoint:** `POST /api/auth/register`
- **Payload:** `{"email": "unique@email.com", "password": "password123", "name": "User Name"}`
- **Expected:** Status 200 with `{"access_token": "...", "token_type": "bearer"}`
- **Tests:** User can create account and receive JWT token

### User Login
- **Endpoint:** `POST /api/auth/login`
- **Payload:** `{"email": "registered@email.com", "password": "password123"}`
- **Expected:** Status 200 with `{"access_token": "...", "token_type": "bearer"}`
- **Tests:** User can authenticate with credentials

### Authentication Required
- **Endpoint:** `GET /api/auth/me` (without token)
- **Expected:** Status 401 "Not authenticated"
- **Tests:** Protected endpoints reject unauthenticated requests

### Authenticated Access
- **Endpoint:** `GET /api/auth/me` (with valid token)
- **Header:** `Authorization: Bearer {token}`
- **Expected:** Status 200 with user data
- **Tests:** Protected endpoints accept valid tokens

### Courses Listing
- **Endpoint:** `GET /api/courses`
- **Header:** `Authorization: Bearer {token}`
- **Expected:** Status 200 with array of courses
- **Tests:** Course data is accessible to authenticated users

### Error Handling
- **Test:** Invalid login credentials return 401
- **Test:** Duplicate email registration returns 400

## Continuous Integration

To use these checks in GitHub Actions or other CI/CD pipelines:

```yaml
name: Check50 Tests
on: [push, pull_request]

jobs:
  check50:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Start backend
        run: |
          cd backend
          python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
          sleep 2
      - name: Run tests
        run: python test_lms.py
```

## Troubleshooting

### "Server is not running" Error
- Make sure to start the backend server first:
  ```bash
  cd backend
  python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
  ```

### "Registration failed" Errors
- These are usually temporary database issues. Run the tests again.
- The test runner uses unique timestamps for email addresses to avoid conflicts.

### Port Already in Use
- Change the port in both commands if 8000 is occupied:
  ```bash
  # Backend
  python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
  
  # Test runner (modify BASE_URL in test_lms.py)
  ```

### Database Issues
- The tests use a fresh database (`fraylon_test.db`) that is automatically cleaned up
- If tests fail, delete any stray test database files and retry

## Architecture

```
LMS-main/
├── .check50.yaml              # Check50 configuration
├── checks/                    # Check module directory
│   └── check50.py            # All check50 test functions
├── test_lms.py               # Windows-friendly test runner
├── backend/
│   ├── requirements.txt       # Updated with requests
│   └── app/
│       ├── main.py           # FastAPI app entry point
│       ├── models.py         # SQLAlchemy models
│       ├── routers/
│       │   ├── auth.py       # Authentication endpoints
│       │   ├── courses.py    # Course endpoints
│       │   └── ...
│       └── ...
└── README.md                 # Updated with check50 instructions
```

## Next Steps

1. **Push to GitHub:** Commit all files and push to your repository
   ```bash
   git add .
   git commit -m "Add check50 automated tests for LMS"
   git push origin main
   ```

2. **Use in Production:** Deploy the LMS and run periodic checks
   ```bash
   check50 Priya056/LMS--PROJECT/main
   ```

3. **Extend Tests:** Add more checks as you add features
   - Problem submission endpoints
   - Chat functionality
   - Lecture endpoints
   - Database transaction tests

4. **Monitor:** Set up GitHub Actions to run tests on every commit

## Support

For issues or questions:
- Check the error messages in the test output
- Review the check50 documentation at: https://github.com/cs50/check50
- Refer to the LMS README.md for general setup

---

**Last Updated:** May 2026
**Framework:** FastAPI + SQLAlchemy + Pydantic
**Python Version:** 3.10+
