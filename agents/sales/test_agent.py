import unittest
from agents.sales.agent import SalesAgent

class TestSalesAgent(unittest.TestCase):
    def test_on_task_received(self):
        agent = SalesAgent()
        result = agent.on_task_received('test sales task')
        self.assertIn('SalesAgent received', result)

if __name__ == '__main__':
    unittest.main()
