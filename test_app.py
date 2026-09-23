import pytest
from app import app, db, Task

@pytest.fixture(scope='function')
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_create_task(client):
    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task.',
        'status': 'todo',
        'priority': 'high',
        'due_date': '2023-12-31'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Task'

def test_get_tasks(client):
    client.post('/tasks', json={
        'title': 'Task 1',
        'description': 'First task.',
        'status': 'done',
        'priority': 'low',
        'due_date': '2023-11-30'
    })
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1

def test_get_task(client):
    task_id = client.post('/tasks', json={
        'title': 'Task 2',
        'description': 'Second task.',
        'status': 'doing',
        'priority': 'medium',
        'due_date': '2023-12-01'
    }).get_json()['id']
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Task 2'

def test_update_task(client):
    task_id = client.post('/tasks', json={
        'title': 'Task 3',
        'description': 'Third task.',
        'status': 'todo',
        'priority': 'high',
        'due_date': '2023-12-02'
    }).get_json()['id']
    response = client.put(f'/tasks/{task_id}', json={
        'title': 'Updated Task 3',
        'description': 'Updated description.',
        'status': 'done',
        'priority': 'low',
        'due_date': '2023-12-03'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Task 3'

def test_delete_task(client):
    task_id = client.post('/tasks', json={
        'title': 'Task 4',
        'description': 'Fourth task.',
        'status': 'doing',
        'priority': 'medium',
        'due_date': '2023-12-04'
    }).get_json()['id']
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Task deleted'
