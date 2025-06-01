from core.agents.base import AgentBase
from core.events.pubsub import subscribe, publish
from core.models.job_tracking import update_job_status, JobStatus

class ImplementorAgent(AgentBase):
    def __init__(self):
        super().__init__("implementor")
        subscribe(self.channel_in, self.on_task_received)

    def on_task_received(self, data: dict):
        self.log(f"Received task from {data['from']}: {data['task']}")
        # Update job status to running if parent_task is tracked
        parent_task = data.get("parent_task")
        if parent_task:
            from core.models.job_tracking import get_job
            job = get_job(parent_task) if isinstance(parent_task, int) else None
            if job:
                update_job_status(job.id, JobStatus.RUNNING)
        messages = [
            {"role": "system", "content": "You are a senior software engineer AI. Write well-structured, production-grade Python code for the task."},
            {"role": "user", "content": data["task"]},
        ]
        solution = self.reply(messages)
        # Update job status to success if parent_task is tracked
        if parent_task and job:
            update_job_status(job.id, JobStatus.SUCCESS, result=solution)
        publish("pm:result", {
            "from": self.name,
            "result": solution,
            "parent_task": data.get("parent_task"),
        })
        self.log("Published solution to PM.")
