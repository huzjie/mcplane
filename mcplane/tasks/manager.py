"""Long-running task manager for the MCP Tasks extension.

Tracks task lifecycle (pending -> running -> completed / failed / cancelled)
with an in-memory store plus optional SQLite persistence.
"""

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ..errors import TaskError


class TaskStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    task_id: str
    server_name: str
    method: str
    status: str = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


class TaskManager:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._lock = threading.Lock()

    def create(self, server_name: str, method: str) -> Task:
        task = Task(task_id=uuid.uuid4().hex, server_name=server_name, method=method)
        with self._lock:
            self._tasks[task.task_id] = task
        return task

    def get(self, task_id: str) -> Task:
        with self._lock:
            task = self._tasks.get(task_id)
        if not task:
            raise TaskError("unknown task: %s" % task_id)
        return task

    def update(self, task_id: str, status: str = None, result: Any = None,
               error: str = None):
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                raise TaskError("unknown task: %s" % task_id)
            if status is not None:
                task.status = status
            if result is not None:
                task.result = result
            if error is not None:
                task.error = error
            task.updated_at = time.time()

    def cancel(self, task_id: str):
        self.update(task_id, status=TaskStatus.CANCELLED)

    def status_dict(self, task_id: str) -> Dict[str, Any]:
        task = self.get(task_id)
        out = {"taskId": task.task_id, "status": task.status}
        if task.result is not None:
            out["result"] = task.result
        if task.error:
            out["error"] = task.error
        return out
