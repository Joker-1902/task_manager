from .conftest import db_session
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
import uuid

client = TestClient(app)

def override_get_db(db_session):
    def get_test_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = get_test_db          



def test_create_task():
    response = client.post('/tasks/', json={'title':'Купить автополироль'})
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Купить автополироль'


def test_create_task_without_title_returns_422():
    response = client.post('/tasks/', json={})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_create_task_returns_valid_uuid_and_shape():
    response = client.post('/tasks/', json={'title': 'Новая задача 4'})
    assert response.status_code == 200
    task = response.json()

    assert 'uuid' in task
    assert 'title' in task
    assert 'status' in task


def test_get_list_of_tasks():
    response = client.get('/tasks/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_empty_list_after_deleting():
    response = client.post('/tasks/', json={'title': 'Новая задача'})
    assert response.status_code == 200

    new_response = client.delete('/tasks/delete_all')
    assert new_response.status_code == 200

    get_all_tasks_response = client.get('/tasks/')
    
    assert get_all_tasks_response.status_code == 200
    assert get_all_tasks_response.json() == []  


def test_get_task_by_uuid():
    response = client.post('/tasks/', json={'title': 'Готовимся у релизу'})
    assert response.status_code == 200
    created_task = response.json()
    task_uuid = created_task['uuid']
    task_to_get = client.get(f'/tasks/{task_uuid}')
    assert task_to_get.status_code == 200


def test_get_not_created_task():
    non_exist_uuid = str(uuid.uuid4())
    response = client.get(f'/tasks/{non_exist_uuid}')
    assert response.status_code == 404


def test_patch_created_task():
    response = client.post('/tasks/', json={'title': 'Готовимся у релизу'})
    assert response.status_code == 200
    created_task = response.json()
    task_uuid = created_task['uuid']
    patch_data = {'status':'done'}
    
    updated_response = client.patch(f'/tasks/{task_uuid}', json=patch_data)
    assert updated_response.status_code == 200   

    updated_task = updated_response.json()
    assert updated_task['status'] == 'done'


def test_patch_not_created_task():
    not_existed_uuid = str(uuid.uuid4())
    update_data = {'status': 'done'}
    not_created_task = client.patch(f'/tasks/{not_existed_uuid}', json=update_data)
    assert not_created_task.status_code == 404



def test_patch_invalid_status_returns_422():
    response = client.post('/tasks/', json={'title': 'Новая задача 3'})
    assert response.status_code == 200
    task = response.json()
    task_uuid = task['uuid']

    bad_response = client.patch(f'/tasks/{task_uuid}', json={'status': 'invalid'})
    assert bad_response.status_code == 422
    assert "detail" in bad_response.json()


def test_delete_tasks():
    response = client.delete('/tasks/delete_all')
    assert response.status_code == 200

    get_empty_list = client.get('/tasks/')
    assert get_empty_list.status_code == 200
    assert get_empty_list.json() == []


def test_delete_by_uuid():
    response = client.post('/tasks/', json={'title': 'Готовимся у релизу'})
    assert response.status_code == 200
    created_task = response.json()
    task_uuid = created_task['uuid']

    response_to_delete = client.delete(f'/tasks/{task_uuid}')
    assert response_to_delete.status_code == 200


def test_delte_not_created_task():
    non_exist_uuid = str(uuid.uuid4())
    response = client.delete(f'/tasks/{non_exist_uuid}')
    assert response.status_code == 404







