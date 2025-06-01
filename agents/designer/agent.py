from core.agents.base import AgentBase
from core.events.pubsub import subscribe, publish
from core.models.job_tracking import update_job_status, JobStatus

class DesignerAgent(AgentBase):
    def __init__(self):
        super().__init__("designer")
        subscribe(self.channel_in, self.on_task_received)

    def on_task_received(self, data: dict):
        self.log(f"Received design request from {data['from']}: {data['task']}")
        parent_task = data.get("parent_task")
        if parent_task:
            from core.models.job_tracking import get_job
            job = get_job(parent_task) if isinstance(parent_task, int) else None
            if job:
                update_job_status(job.id, JobStatus.RUNNING)
        messages = [
            {"role": "system", "content": "You are a senior product designer AI. Convert product ideas into user experience wireframes and feature lists."},
            {"role": "user", "content": data["task"]},
        ]
        design = self.reply(messages)
        if parent_task and job:
            update_job_status(job.id, JobStatus.SUCCESS, result=design)
        publish("pm:result", {
            "from": self.name,
            "result": design,
            "parent_task": data.get("parent_task")
        })
        self.log("Published design result to PM.")
