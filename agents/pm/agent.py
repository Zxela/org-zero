from core.agents.base import AgentBase
from core.events.pubsub import subscribe, publish
from core.models.job_tracking import create_job, update_job_status, JobStatus

class ProjectManagerAgent(AgentBase):
    def __init__(self):
        super().__init__("pm")
        subscribe(self.channel_in, self.on_task_received)
        # Track outstanding tasks and results
        self.active_tasks = {}
        self.results = {}

    def on_task_received(self, data: dict):
        self.log(f"Received task from {data['from']}: {data['task']}")
        # Create a persistent job for this project task
        job = create_job(job_type="project_task", payload=data["task"])
        messages = [
            {"role": "system", "content": "You are a PM AI. Break the product idea into concrete tasks. Assign each to implementor, designer, or devops as appropriate. Return a list of tasks with assignees."},
            {"role": "user", "content": data["task"]},
        ]
        breakdown = self.reply(messages)
        self.log("Project Plan:")
        self.log(breakdown)
        tasks = self.parse_breakdown(breakdown)
        self.active_tasks[data['task']] = {"tasks": tasks, "from": data['from'], "results": {}, "job_id": job.id}
        for t in tasks:
            agent_channel = f"{t['assignee']}:task"
            publish(agent_channel, {"from": "pm", "task": t['description'], "parent_task": data['task']})
        subscribe("pm:result", self.on_result_received)

    def on_result_received(self, data: dict):
        parent_task = data.get('parent_task')
        if not parent_task or parent_task not in self.active_tasks:
            return
        self.active_tasks[parent_task]["results"][data['from']] = data['result']
        # Check if all subtasks are done
        if len(self.active_tasks[parent_task]["results"]) == len(self.active_tasks[parent_task]["tasks"]):
            summary = self.aggregate_results(self.active_tasks[parent_task]["results"])
            publish("director:result", {"from": "pm", "result": summary, "task": parent_task})
            self.log(f"Reported results to director for task: {parent_task}")
            # Update job status to success and store result
            job_id = self.active_tasks[parent_task].get("job_id")
            if job_id:
                update_job_status(job_id, JobStatus.SUCCESS, result=summary)
            del self.active_tasks[parent_task]

    def parse_breakdown(self, breakdown):
        # Dummy parser: expects lines like "[implementor] Build API"
        tasks = []
        for line in breakdown.split('\n'):
            if line.strip().startswith('['):
                try:
                    assignee = line.split(']')[0][1:]
                    desc = line.split(']')[1].strip()
                    tasks.append({"assignee": assignee, "description": desc})
                except Exception:
                    continue
        return tasks

    def aggregate_results(self, results):
        # Simple aggregation: join all results
        return '\n'.join(f"{k}: {v}" for k, v in results.items())
