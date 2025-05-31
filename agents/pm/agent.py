from core.agents.base import AgentBase
from core.events.pubsub import subscribe, publish

class ProjectManagerAgent(AgentBase):
    def __init__(self):
        super().__init__("pm")
        subscribe(self.channel_in, self.on_task_received)

    def on_task_received(self, data: dict):
        self.log(f"Received task from {data['from']}: {data['task']}")

        # For now, simulate a plan
        messages = [
            {"role": "system", "content": "You are a PM AI. Break the product idea into concrete tasks."},
            {"role": "user", "content": data["task"]},
        ]
        breakdown = self.reply(messages)

        self.log("Project Plan:")
        self.log(breakdown)

        publish(self.channel_out if isinstance(self.channel_out, str) else "updates", {
            "from": "pm",
            "plan": breakdown
        })
