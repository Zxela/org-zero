import unittest
from unittest.mock import patch, MagicMock
from agents.pm.agent import ProjectManagerAgent

class TestProjectManagerAgent(unittest.TestCase):
    @patch('agents.pm.agent.publish')
    @patch('agents.pm.agent.subscribe')
    @patch.object(ProjectManagerAgent, 'reply', return_value='[implementor] Build API\n[designer] Design UI')
    def test_on_task_received_and_result_aggregation(self, mock_reply, mock_subscribe, mock_publish):
        agent = ProjectManagerAgent()
        data = {'from': 'director', 'task': 'Build a to-do app.'}
        agent.on_task_received(data)
        # Should parse two tasks and publish to both channels
        self.assertIn(data['task'], agent.active_tasks)
        tasks = agent.active_tasks[data['task']]['tasks']
        self.assertEqual(len(tasks), 2)
        mock_publish.assert_any_call('implementor:task', {'from': 'pm', 'task': 'Build API', 'parent_task': data['task']})
        mock_publish.assert_any_call('designer:task', {'from': 'pm', 'task': 'Design UI', 'parent_task': data['task']})
        # Simulate results from both agents
        agent.on_result_received({'from': 'implementor', 'result': 'API done', 'parent_task': data['task']})
        agent.on_result_received({'from': 'designer', 'result': 'UI done', 'parent_task': data['task']})
        # After both results, should aggregate and publish to director
        mock_publish.assert_any_call('director:result', {'from': 'pm', 'result': 'implementor: API done\ndesigner: UI done', 'task': data['task']})
        self.assertNotIn(data['task'], agent.active_tasks)

if __name__ == '__main__':
    unittest.main()
