from mcplane.tasks.manager import TaskManager, TaskStatus
from mcplane.errors import TaskError


def test_task_lifecycle():
    tm = TaskManager()
    task = tm.create("echo", "tools/call")
    assert task.status == TaskStatus.PENDING
    tm.update(task.task_id, status=TaskStatus.RUNNING)
    tm.update(task.task_id, status=TaskStatus.COMPLETED, result={"ok": True})
    d = tm.status_dict(task.task_id)
    assert d["status"] == "completed"
    assert d["result"] == {"ok": True}


def test_cancel():
    tm = TaskManager()
    task = tm.create("echo", "tools/call")
    tm.cancel(task.task_id)
    assert tm.get(task.task_id).status == TaskStatus.CANCELLED


def test_unknown_task():
    tm = TaskManager()
    try:
        tm.get("nope")
        assert False
    except TaskError:
        pass
