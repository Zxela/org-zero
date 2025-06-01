import unittest
from unittest.mock import patch
from agents.designer.agent import DesignerAgent

class TestDesignerAgent(unittest.TestCase):
    @patch('agents.designer.agent.publish')
    @patch.object(DesignerAgent, 'reply', return_value='Wireframe and feature list')
    def test_on_task_received(self, mock_reply, mock_publish):
        agent = DesignerAgent()
        data = {'from': 'pm', 'task': 'Design a to-do app.', 'parent_task': 'Build a to-do app.'}
        agent.on_task_received(data)
        mock_reply.assert_called_once()
        mock_publish.assert_called_once()
        published_data = mock_publish.call_args[0][1]
        self.assertEqual(published_data['from'], 'designer')
        self.assertEqual(published_data['parent_task'], 'Build a to-do app.')
        self.assertIn('Wireframe and feature list', published_data['result'])

if __name__ == '__main__':
    unittest.main()
