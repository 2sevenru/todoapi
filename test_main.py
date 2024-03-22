from fastapi.testclient import TestClient

from main import app

_token = 'srs11-pwiw9-g3dxt-yblkb'

client = TestClient(app=app)


def test_check_connection():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'result': True, "message": "Connection OK"}


def test_get_tasks():
    response = client.get("/tasks/", headers={'token': _token})
    assert response.status_code == 200
    data = response.json()
    assert 'result' in data and data['result'] is True


def test_unauth_get_tasks():
    response = client.get("/tasks/", headers={'token': 'wrong_token'})
    assert response.status_code == 401


def test_create_task():
    response = client.post("/tasks/?text=test&description=test", headers={'token': _token})
    assert response.status_code == 201
    data = response.json()
    assert 'result' in data and data['result'] is True


def test_fail_create_task():
    response = client.post("/tasks/?text=test", headers={'token': _token})
    assert response.status_code == 422


def test_unauth_create_task():
    response = client.post("/tasks/?text=test&description=test", headers={'token': 'wrong_token'})
    assert response.status_code == 401


def test_read_task():
    response = client.get("/tasks/1", headers={'token': _token})
    assert response.status_code == 200
    data = response.json()
    assert 'result' in data and data['result'] is True


def test_not_found_read_task():
    response = client.get("/tasks/500", headers={'token': _token})
    assert response.status_code == 404


def test_invalid_read_task():
    response = client.get("/tasks/notInt", headers={'token': _token})
    assert response.status_code == 422


def test_unauth_read_task():
    response = client.get("/tasks/1", headers={'token': 'wrong_token'})
    assert response.status_code == 401


def test_update_task():
    response = client.put("/tasks/1?text=test&description=test", headers={'token': _token})
    assert response.status_code == 201
    data = response.json()
    assert 'result' in data and data['result'] is True


def test_no_data_update_task():
    response = client.put("/tasks/1", headers={'token': _token})
    assert response.status_code == 400
    data = response.json()
    assert 'result' in data and data['result'] is False


def test_not_found_update_task():
    response = client.put("/tasks/100?text=test", headers={'token': _token})
    assert response.status_code == 404
    data = response.json()
    assert 'result' in data and data['result'] is False


def test_invalid_update_task():
    response = client.put("/tasks/notInt", headers={'token': _token})
    assert response.status_code == 422


def test_unauth_update_task():
    response = client.put("/tasks/1?text=test&description=test", headers={'token': 'wrong_token'})
    assert response.status_code == 401


def test_delete_task():
    response = client.delete("/tasks/1", headers={'token': _token})
    assert response.status_code == 200
    data = response.json()
    assert 'result' in data and data['result'] is True


def test_not_found_delete_task():
    response = client.delete("/tasks/100", headers={'token': _token})
    assert response.status_code == 404
    data = response.json()
    assert 'result' in data and data['result'] is False


def test_invalid_delete_task():
    response = client.delete("/tasks/notInt", headers={'token': _token})
    assert response.status_code == 422


def test_unauth_delete_task():
    response = client.delete("/tasks/1", headers={'token': 'wrong_token'})
    assert response.status_code == 401


def test_users_create():
    response = client.post("/users/create?login=testLogin")
    assert response.status_code == 201
    data = response.json()
    assert 'result' in data and data['result'] is True


def test_get_user():
    response = client.get("/users/get", headers={'token': _token})
    assert response.status_code == 200
    data = response.json()
    assert 'result' in data and data['result'] is True


def test_unauth_get_user():
    response = client.get("/users/get", headers={'token': "wrong_token"})
    assert response.status_code == 401

# pytest: 22 passed
