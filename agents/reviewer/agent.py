from core.agents.base import AgentBase
from core.events.pubsub import subscribe, publish

class ReviewerAgent(AgentBase):
    def __init__(self):
        super().__init__("reviewer")
        subscribe(self.channel_in, self.on_task_received)

    def on_task_received(self, data: dict):
        self.log(f"Received review task from {data['from']}: {data['task']}")
        messages = [
            {"role": "system", "content": "You are a senior code reviewer AI. Analyze and suggest improvements to the submitted implementation."},
            {"role": "user", "content": data["task"]},
        ]
        review = self.reply(messages)
        publish("pm:result", {
            "from": self.name,
            "result": review,
            "parent_task": data.get("parent_task")
        })
        self.log("Published review result to PM.")
