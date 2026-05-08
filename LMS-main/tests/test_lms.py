import pytest
import json
from models import db, User, Problem

def test_app_loads(app):
    assert app is not None
    assert app.config['TESTING'] is True

def test_home_page(client):
    response = client.get('/')
    assert response.status_code in [200, 302]

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_invalid_login(client):
    response = client.post('/login', data={'email': 'wrong@example.com', 'password': 'bad'})
    assert response.status_code in [200, 302, 400]

def test_protected_route(app):
    fresh_client = app.test_client()
    fresh_client.get('/logout')
    response = fresh_client.get('/dashboard')
    assert response.status_code == 302

@pytest.fixture
def auth_client(app):
    from werkzeug.security import generate_password_hash
    client = app.test_client()
    with app.app_context():
        user = User.query.filter_by(email='testuser@example.com').first()
        if not user:
            user = User(email='testuser@example.com', password=generate_password_hash('password123'), name='Test User')
            db.session.add(user)
            db.session.commit()
    client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'})
    return client

def test_lecture_page(auth_client):
    response = auth_client.get('/lecture/cs50p/lecture_0')
    assert response.status_code == 200

def test_problems_exist(app):
    with app.app_context():
        problems = Problem.query.filter_by(lecture_id='lecture_0').all()
        assert len(problems) >= 5

def test_problem_hello_world(auth_client):
    response = auth_client.get('/lecture/cs50p/lecture_0')
    assert b"Hello World" in response.data

def test_problem_sum(auth_client):
    response = auth_client.get('/lecture/cs50p/lecture_0')
    assert b"Sum of Two Numbers" in response.data

def test_problem_even_odd(auth_client):
    response = auth_client.get('/lecture/cs50p/lecture_0')
    assert b"Even or Odd" in response.data

def test_problem_square(auth_client):
    response = auth_client.get('/lecture/cs50p/lecture_0')
    assert b"Square of a Number" in response.data

def test_problem_calculator(auth_client):
    response = auth_client.get('/lecture/cs50p/lecture_0')
    assert b"Simple Calculator" in response.data
