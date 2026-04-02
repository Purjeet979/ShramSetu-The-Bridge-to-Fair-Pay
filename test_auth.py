import pytest
from app import app
import database

from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_unauthorized_access(client):
    """Test that protected routes redirect to login when no JWT is present."""
    response = client.get('/', follow_redirects=True)
    # The message comes from unauthorized_callback in app.py
    assert b"Please login first!" in response.data
    assert b"Welcome Back" in response.data

def test_login_success(client):
    """Test successful login issues a JWT cookie."""
    # Seed a test user
    conn = database.get_connection()
    if not conn:
        pytest.skip("MySQL not running locally")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE identifier = 'test@example.com'")
    cursor.execute("INSERT INTO users (name, identifier, password_hash, role) VALUES ('Test User', 'test@example.com', 'testpass', 'Admin')")
    conn.commit()
    conn.close()

    response = client.post('/login', data={
        'identifier': 'test@example.com',
        'password': 'testpass'
    })
    
    assert response.status_code == 302
    assert response.location.split('/')[-2] == "" # Check if redirecting to root
    # Check for JWT cookie in set-cookie headers
    cookie_found = any('access_token_cookie' in h[1] for h in response.headers if h[0] == 'Set-Cookie')
    assert cookie_found

def test_logout(client):
    """Test logout clears JWT cookies."""
    # First login (we skip this if MySQL isn't running as per test_login_success)
    client.post('/login', data={'identifier': 'test@example.com', 'password': 'testpass'})
    
    # Then logout
    response = client.get('/logout', follow_redirects=True)
    assert b"You have been logged out." in response.data
    # Check for unset cookie
    cookie_cleared = any('access_token_cookie=;' in h[1] for h in response.headers if h[0] == 'Set-Cookie')
    assert cookie_cleared
