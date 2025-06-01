import unittest
from unittest.mock import patch
from agents.reviewer.agent import ReviewerAgent

class TestReviewerAgent(unittest.TestCase):
    @patch('agents.reviewer.agent.publish')
    @patch.object(ReviewerAgent, 'reply', return_value='Looks good, but add tests.')
    def test_on_task_received(self, mock_reply, mock_publish):
        agent = ReviewerAgent()
        data = {'from': 'pm', 'task': 'Review the API code.', 'parent_task': 'Build a to-do app.'}
        agent.on_task_received(data)
        mock_reply.assert_called_once()
        mock_publish.assert_called_once()
        published_data = mock_publish.call_args[0][1]
        self.assertEqual(published_data['from'], 'reviewer')
        self.assertEqual(published_data['parent_task'], 'Build a to-do app.')
        self.assertIn('Looks good, but add tests.', published_data['result'])

if __name__ == '__main__':
    unittest.main()
