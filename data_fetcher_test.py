#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from unittest.mock import patch, MagicMock
from data_fetcher import run_query, get_user_sensor_data, get_user_workouts, get_user_profile, get_user_posts
from google.cloud import bigquery

class TestDataFetcher(unittest.TestCase):
    @patch('data_fetcher.client.query')
    def test_run_query(self, mock_query):
        """Tests the run_query function."""
        # Arrange
        mock_query_job = MagicMock()
        mock_query.return_value = mock_query_job
        # Mocking the .result() method to directly return the desired rows
        mock_query_job.result.return_value = [
            bigquery.table.Row(('val1', 'val2'), {'col1': 0, 'col2': 1}),
            bigquery.table.Row(('val3', 'val4'), {'col1': 0, 'col2': 1})
        ]

        query = "SELECT * FROM `CIS4993.Workouts`"  # changed to SomeTable, which was an error on a previous run

        # Act
        result = run_query(query)

        # Assert
        mock_query.assert_called_once_with(query)
        # Assert that the .result() method was called, it is now mocked so it should not fail
        mock_query_job.result.assert_called_once()
        self.assertEqual(result, [
            {'col1': 'val1', 'col2': 'val2'},
            {'col1': 'val3', 'col2': 'val4'}
        ])

    @patch('data_fetcher.run_query')
    def test_get_user_sensor_data(self, mock_run_query):
      
        mock_run_query.return_value = [
            {'WorkoutID': 'workout1', 'timestamp': '2024-02-29T10:00:00', 'SensorValue': 100, 'Name': 'Heart Rate', 'Units': 'BPM'},
            {'WorkoutID': 'workout1', 'timestamp': '2024-02-29T10:00:01', 'SensorValue': 102, 'Name': 'Heart Rate', 'Units': 'BPM'}
        ]

        user_id = "user1"
        workout_id = "workout1"

        result = get_user_sensor_data(user_id, workout_id)

        mock_run_query.assert_called_once()
        query = mock_run_query.call_args[0][0]

        self.assertIn("FROM `CIS4993.SensorData` AS sd", query)
        self.assertIn("JOIN `CIS4993.SensorTypes` AS st", query)
        self.assertIn("JOIN `CIS4993.Workouts` AS w", query)
        self.assertIn("WHERE w.UserId = 'user1' AND sd.WorkoutID = 'workout1'", query)
        self.assertIn("ORDER BY sd.timestamp", query)

        self.assertEqual(result, [
            {'WorkoutID': 'workout1', 'timestamp': '2024-02-29T10:00:00', 'SensorValue': 100, 'Name': 'Heart Rate', 'Units': 'BPM'},
            {'WorkoutID': 'workout1', 'timestamp': '2024-02-29T10:00:01', 'SensorValue': 102, 'Name': 'Heart Rate', 'Units': 'BPM'}
        ])
        
    @patch('data_fetcher.run_query')
    def test_get_user_workouts(self, mock_run_query):
        """Tests the get_user_workouts function."""
        # Arrange
        mock_run_query.return_value = [
            {'WorkoutID': 'workout1', 'StartTimeStamp': '2024-02-29T08:00:00', 'EndTimeStamp': '2024-02-29T09:00:00', 'TotalDistance': 5.0, 'TotalSteps': 6000, 'CaloriesBurned': 300},
            {'WorkoutID': 'workout2', 'StartTimeStamp': '2024-02-28T09:00:00', 'EndTimeStamp': '2024-02-28T10:00:00', 'TotalDistance': 6.0, 'TotalSteps': 7000, 'CaloriesBurned': 350}
        ]
        user_id = "user1"

        # Act
        result = get_user_workouts(user_id)

        # Assert
        mock_run_query.assert_called_once()
        query = mock_run_query.call_args[0][0]
        self.assertIn("FROM `ise-w-genai.CIS4993.Workouts`", query)
        self.assertIn("WHERE UserId = 'user1'", query)
        self.assertIn("ORDER BY StartTimeStamp DESC", query)
        self.assertEqual(result, [
            {'WorkoutID': 'workout1', 'StartTimeStamp': '2024-02-29T08:00:00', 'EndTimeStamp': '2024-02-29T09:00:00', 'TotalDistance': 5.0, 'TotalSteps': 6000, 'CaloriesBurned': 300},
            {'WorkoutID': 'workout2', 'StartTimeStamp': '2024-02-28T09:00:00', 'EndTimeStamp': '2024-02-28T10:00:00', 'TotalDistance': 6.0, 'TotalSteps': 7000, 'CaloriesBurned': 350}
        ])

    @patch('data_fetcher.run_query')
    def test_get_user_profile(self, mock_run_query):
        """Tests the get_user_profile function."""
        # Arrange
        mock_run_query.return_value = [
            {'UserId': 'user1', 'Name': 'Test User', 'Username': 'testuser', 'DateOfBirth': '1990-01-01', 'ImageUrl': 'http://test.com/image.jpg'}
        ]
        user_id = "user1"

        # Act
        result = get_user_profile(user_id)

        # Assert
        mock_run_query.assert_called_once()
        query = mock_run_query.call_args[0][0]
        self.assertIn("FROM `ise-w-genai.CIS4993.Users`", query)
        self.assertIn("WHERE UserId = 'user1'", query)
        self.assertEqual(result, {'UserId': 'user1', 'Name': 'Test User', 'Username': 'testuser', 'DateOfBirth': '1990-01-01', 'ImageUrl': 'http://test.com/image.jpg'})

    @patch('data_fetcher.run_query')
    def test_get_user_profile_no_user(self, mock_run_query):
        """Tests get_user_profile when no user is found."""
        # Arrange
        mock_run_query.return_value = []
        user_id = "nonexistentuser"

        # Act
        result = get_user_profile(user_id)

        # Assert
        mock_run_query.assert_called_once()
        query = mock_run_query.call_args[0][0]
        self.assertIn("FROM `ise-w-genai.CIS4993.Users`", query)
        self.assertIn("WHERE UserId = 'nonexistentuser'", query)
        self.assertIsNone(result)
        
    @patch('data_fetcher.run_query')
    def test_get_user_posts(self, mock_run_query):
        """Tests the get_user_posts function."""
        # Arrange
        mock_run_query.return_value = [
            {'PostId': 'post1', 'AuthorId': 'user1', 'Timestamp': '2024-02-29T10:00:00', 'Content': 'Test post 1', 'ImageUrl': 'http://test.com/post1.jpg'},
            {'PostId': 'post2', 'AuthorId': 'user1', 'Timestamp': '2024-02-28T12:00:00', 'Content': 'Test post 2', 'ImageUrl': 'http://test.com/post2.jpg'}
        ]
        user_id = "user1"

        # Act
        result = get_user_posts(user_id)

        # Assert
        mock_run_query.assert_called_once()
        query = mock_run_query.call_args[0][0]
        self.assertIn("FROM `ise-w-genai.CIS4993.Posts`", query)
        self.assertIn("WHERE AuthorId = 'user1'", query)
        self.assertIn("ORDER BY Timestamp DESC", query)
        self.assertEqual(result, [
            {'PostId': 'post1', 'AuthorId': 'user1', 'Timestamp': '2024-02-29T10:00:00', 'Content': 'Test post 1', 'ImageUrl': 'http://test.com/post1.jpg'},
            {'PostId': 'post2', 'AuthorId': 'user1', 'Timestamp': '2024-02-28T12:00:00', 'Content': 'Test post 2', 'ImageUrl': 'http://test.com/post2.jpg'}
        ])


if __name__ == "__main__":
    unittest.main()
