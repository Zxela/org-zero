import unittest
from unittest.mock import patch, MagicMock
from agents.implementor.agent import ImplementorAgent

class TestImplementorAgent(unittest.TestCase):
    @patch('agents.implementor.agent.publish')
    @patch.object(ImplementorAgent, 'reply', return_value='Here is the implemented solution.')
    def test_on_task_received(self, mock_reply, mock_publish):
        agent = ImplementorAgent()
        task_data = {
            "from": "pm",
            "task": "Create a simple REST API using FastAPI.",
            "parent_task": "Build a to-do app"
        }

        agent.on_task_received(task_data)

        mock_reply.assert_called_once()
        mock_publish.assert_called_once()
        published_data = mock_publish.call_args[0][1]
        self.assertEqual(published_data["from"], "implementor")
        self.assertEqual(published_data["parent_task"], "Build a to-do app")
        self.assertIn("Here is the implemented solution", published_data["result"])

if __name__ == '__main__':
    unittest.main()
