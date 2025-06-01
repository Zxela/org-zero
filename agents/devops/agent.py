from core.agents.base import AgentBase
from core.models.job_tracking import update_job_status, JobStatus

class DevOpsAgent(AgentBase):
    def __init__(self):
        super().__init__(name="devops")

    def on_task_received(self, task):
        # Job tracking is optional for devops, but if parent_task is provided, update job status
        parent_task = getattr(task, 'parent_task', None) if hasattr(task, 'parent_task') else None
        if parent_task:
            from core.models.job_tracking import get_job
            job = get_job(parent_task) if isinstance(parent_task, int) else None
            if job:
                update_job_status(job.id, JobStatus.RUNNING)
        result = f"DevOpsAgent received: {task}"
        if parent_task and job:
            update_job_status(job.id, JobStatus.SUCCESS, result=result)
        return result