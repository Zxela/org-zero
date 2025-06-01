from core.agents.base import AgentBase

class SalesAgent(AgentBase):
    def __init__(self):
        super().__init__(name="sales")

    def on_task_received(self, task):
        return f"SalesAgent received: {task}"