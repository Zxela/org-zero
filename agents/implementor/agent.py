from core.agents.base import AgentBase
from core.events.pubsub import subscribe, publish

class ImplementorAgent(AgentBase):
    def __init__(self):
        super().__init__("implementor")
        subscribe(self.channel_in, self.on_task_received)

    def on_task_received(self, data: dict):
        self.log(f"Received task from {data['from']}: {data['task']}")
        messages = [
            {"role": "system", "content": "You are a senior software engineer AI. Write well-structured, production-grade Python code for the task."},
            {"role": "user", "content": data["task"]},
        ]
        solution = self.reply(messages)

        # You could add filesystem write here if desired
        publish("pm:result", {
            "from": self.name,
            "result": solution,
            "parent_task": data.get("parent_task"),
        })
        self.log("Published solution to PM.")
