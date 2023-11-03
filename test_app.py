# test_app.py
import pytest
from app import app, get_tasks


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_add_task(client):
    response = client.post(
        '/add', data={'task': 'Test Task'}, follow_redirects=True)
    assert 'Test Task' in response.get_data(as_text=True)


def test_remove_task(client):
    # Add a task first
    client.post('/add', data={'task': 'Task to Remove'}, follow_redirects=True)

    # Check if the task is in the tasks dictionary before removal
    tasks_before_removal = get_tasks()
    assert 'Task to Remove' in tasks_before_removal

    # Remove the task
    client.post(
        '/remove', data={'task': 'Task to Remove'}, follow_redirects=True)

    # Check if the task is not in the tasks dictionary after removal
    tasks_after_removal = get_tasks()
    assert 'Task to Remove' not in tasks_after_removal
