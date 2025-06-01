from core.agents.base import AgentBase

class DevOpsAgent(AgentBase):
    def __init__(self):
        super().__init__(name="devops")

    def on_task_received(self, task):
        return f"DevOpsAgent received: {task}"