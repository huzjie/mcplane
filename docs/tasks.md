# 长任务扩展（Tasks）

`TaskManager` 管理长任务生命周期：`pending → running → completed/failed/cancelled`。

```python
from mcplane.tasks.manager import TaskManager

tm = TaskManager()
task = tm.create("echo", "tools/call")
tm.update(task.task_id, status="running")
tm.update(task.task_id, status="completed", result={"content": []})
print(tm.status_dict(task.task_id))
```
