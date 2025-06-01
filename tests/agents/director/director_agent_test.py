import unittest
from unittest.mock import patch, MagicMock
from agents.director.agent import DirectorAgent

class TestDirectorAgent(unittest.TestCase):
    @patch('agents.director.agent.publish')
    @patch.object(DirectorAgent, 'reply', return_value='Test task description')
    def test_handle_user_input(self, mock_reply, mock_publish):
        agent = DirectorAgent()
        user_message = 'Build a to-do app.'
        response = agent.handle_user_input(user_message)
        self.assertIn('I\'ve handed your request to the PM', response)
        mock_reply.assert_called_once()
        mock_publish.assert_called_once()

if __name__ == '__main__':
    unittest.main()
