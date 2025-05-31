from core.agents.base import AgentBase
from core.events.pubsub import publish

class DirectorAgent(AgentBase):
    def __init__(self):
        super().__init__("director")

    def handle_user_input(self, user_message: str) -> str:
        messages = [
            {"role": "system", "content": "You are a director AI. Understand product ideas and delegate to the PM."},
            {"role": "user", "content": user_message},
        ]
        task_description = self.reply(messages)

        self.log(f"Delegating to PM: {task_description}")
        publish(self.channel_out, {
            "from": "director",
            "task": task_description
        })

        return f"I've handed your request to the PM. Task: {task_description}"
