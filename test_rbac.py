import pytest
from app import app
import database
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    with app.test_client() as client:
        yield client

def test_role_access_admin(client):
    """Admin should have access to admin routes."""
    with app.app_context():
        access_token = create_access_token(identity="1", additional_claims={"role": "Admin"})
    
    client.set_cookie('access_token_cookie', access_token)
    
    # Test an admin-only route
    response = client.get('/admin/approve_logs')
    assert response.status_code == 200

def test_role_access_supervisor(client):
    """Supervisor should NOT have access to admin routes but SHOULD have access to supervisor routes."""
    with app.app_context():
        access_token = create_access_token(identity="2", additional_claims={"role": "Supervisor"})
    
    client.set_cookie('access_token_cookie', access_token)
    
    # Test an admin-only route (should fail)
    response = client.get('/admin/approve_logs', follow_redirects=True)
    assert b"Access Denied" in response.data
    
    # Test a supervisor-accessible route
    response = client.get('/record_work')
    assert response.status_code == 200

def test_role_access_worker(client):
    """Worker should NOT have access to supervisor/admin routes."""
    with app.app_context():
        access_token = create_access_token(identity="3", additional_claims={"role": "Worker"})
    
    client.set_cookie('access_token_cookie', access_token)
    
    # Test supervisor route (should fail)
    response = client.get('/record_work', follow_redirects=True)
    assert b"Access Denied" in response.data
    
    # Test admin route (should fail)
    response = client.get('/admin/approve_logs', follow_redirects=True)
    assert b"Access Denied" in response.data
    
    # Test worker dashboard (index)
    response = client.get('/')
    assert response.status_code == 200
    assert b"My Work Records" in response.data or b"Total Pending Wages" in response.data
