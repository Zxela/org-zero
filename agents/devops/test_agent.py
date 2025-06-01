import unittest
from agents.devops.agent import DevOpsAgent

class TestDevOpsAgent(unittest.TestCase):
    def test_on_task_received(self):
        agent = DevOpsAgent()
        result = agent.on_task_received('test devops task')
        self.assertIn('DevOpsAgent received', result)

if __name__ == '__main__':
    unittest.main()
