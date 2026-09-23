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
    assert len(data['items']) == 1

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

def test_text_search(client):
    client.post('/tasks', json={
        'title': 'Search Task',
        'description': 'This task should be found.',
        'status': 'todo',
        'priority': 'high',
        'due_date': '2023-12-31'
    })
    response = client.get('/tasks?q=Search')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 1

def test_status_filter(client):
    client.post('/tasks', json={
        'title': 'Status Task',
        'description': 'This task should be found.',
        'status': 'done',
        'priority': 'low',
        'due_date': '2023-11-30'
    })
    response = client.get('/tasks?status=done')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 1

def test_priority_filter(client):
    client.post('/tasks', json={
        'title': 'Priority Task',
        'description': 'This task should be found.',
        'status': 'todo',
        'priority': 'medium',
        'due_date': '2023-12-01'
    })
    response = client.get('/tasks?priority=medium')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 1

def test_combined_filter(client):
    client.post('/tasks', json={
        'title': 'Combined Task',
        'description': 'This task should be found.',
        'status': 'done',
        'priority': 'low',
        'due_date': '2023-11-30'
    })
    response = client.get('/tasks?q=Combined&status=done')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 1

def test_invalid_status(client):
    response = client.get('/tasks?status=invalid')
    assert response.status_code == 422

def test_invalid_priority(client):
    response = client.get('/tasks?priority=invalid')
    assert response.status_code == 422

def test_get_unknown_id(client):
    response = client.get('/tasks/999')
    assert response.status_code == 404
