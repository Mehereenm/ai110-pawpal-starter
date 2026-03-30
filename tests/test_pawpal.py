import pytest
from pawpal_system import Task, Pet

def test_task_completion():
    """Verify that calling mark_complete() changes the task's completion status."""
    task = Task(
        description="Test Task",
        category="test",
        time=10,
        priority=3,
        frequency="daily",
        preferred_time="morning"
    )
    # Initially not complete
    assert not task.completion_status
    # Mark as complete
    task.mark_complete()
    # Now should be complete
    assert task.completion_status

def test_task_addition():
    """Verify that adding a task to a Pet increases the pet's task count."""
    pet = Pet(
        name="Test Pet",
        species="Dog",
        age=2,
        special_needs=[]
    )
    initial_count = len(pet.tasks)
    task = Task(
        description="New Task",
        category="exercise",
        time=20,
        priority=4,
        frequency="daily",
        preferred_time="afternoon"
    )
    pet.add_task(task)
    assert len(pet.tasks) == initial_count + 1
