#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""
    @patch("modules.create_component") #genAI used to consult about mock, no code taken directly from it
    def test_display_post(self, mock_create_component):

        username = "roary"
        user_image = "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg"
        timestamp = "01-01-1900"
        content = "This is a test"
        post_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Ludovic_and_Lauren_%288425515069%29.jpg/330px-Ludovic_and_Lauren_%288425515069%29.jpg"

        display_post(username, user_image, timestamp, content, post_image)
        
        expected_data = {
            'username': username,
            'user_image': user_image,
            'timestamp': timestamp,
            'content': content,
            'post_image': post_image
        }

        mock_create_component.assert_called_once_with(expected_data, "post", 600)


        


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""
    
    @patch("modules.create_component")
    def test_display_activity_summary(self, mock_create_component): 
        workouts_list = [
            [
                {
                    "distance": 5.2,
                    "start_timestamp": "2023-06-01T10:30:00",
                    "end_timestamp": "2023-06-01T11:15:00",
                    "calories_burned": 350,
                    "steps": 6500
                }
            ],
            [
                {
                    "distance": 3.8,
                    "start_timestamp": "2023-06-02T08:00:00",
                    "end_timestamp": "2023-06-02T08:45:00",
                    "calories_burned": 280,
                    "steps": 4800
                }
            ]
        ]
        
        dates, steps, calories, distance, time = display_activity_summary(workouts_list)
        
        expected_data = {
            'TOTAL_DISTANCE': 9.0,
            'TOTAL_MINUTES': 90,
            'TOTAL_CALORIES': 630,
            'TOTAL_STEPS': 11300,
            'TOTAL_WORKOUTS': 2,
            'TOTAL_TIME': 90
        }
        
        # Check that create_component was called with the right arguments
        mock_create_component.assert_called_once_with(expected_data, "display_summary", height=250)
        
        # Check that the returned lists are correct
        self.assertEqual(dates, ["06-01", "06-02"])
        self.assertEqual(steps, [6500, 4800])
        self.assertEqual(calories, [350, 280])
        self.assertEqual(distance, [5.2, 3.8])
        self.assertEqual(time, [45, 45])

    @patch("modules.create_component")
    def test_display_activity_summary_empty_list(self, mock_create_component):
        """Tests that display_activity_summary handles an empty workouts list correctly."""
        # Test with an empty list
        workouts_list = []
        

        dates, steps, calories, distance, time = display_activity_summary(workouts_list)
        
        expected_data = {
            'TOTAL_DISTANCE': 0,
            'TOTAL_MINUTES': 0,
            'TOTAL_CALORIES': 0,
            'TOTAL_STEPS': 0,
            'TOTAL_WORKOUTS': 0,
            'TOTAL_TIME': 0
        }
        

        mock_create_component.assert_called_once_with(expected_data, "display_summary", height=250)
        
        # Check that the returned lists are empty
        self.assertEqual(dates, [])
        self.assertEqual(steps, [])
        self.assertEqual(calories, [])
        self.assertEqual(distance, [])
        self.assertEqual(time, [])
    

class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""
    @patch("modules.create_component")
    def test_display_genai_advice(self, mock_create_component):
        """Tests foo."""
        timestamp = "01-01-1900"
        content = "This is a test"
        post_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Ludovic_and_Lauren_%288425515069%29.jpg/330px-Ludovic_and_Lauren_%288425515069%29.jpg"

        display_genai_advice(timestamp, content, post_image)
        
        expected_data = {
            'timestamp': timestamp,
            'content': content,
            'post_image': post_image
        }

        mock_create_component.assert_called_once_with(expected_data, "gen_ai_display", 600)


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def setUp(self):
        """Initialize AppTest before each test with required parameters."""
        self.app = AppTest(display_recent_workouts, default_timeout=10)

    def test_no_workouts(self):
        """Tests when there are no recent workouts."""
        result = self.app.run([])
        self.assertIn("No recent workouts available.", result.output)

    def test_single_workout(self):
        """Tests displaying a single workout."""
        workouts = [{
            "start_time": " 08:00:00",
            "end_time": "08:30:00",
            "date": "2024-02-19",
            "workout_id": "workout0",
            "distance": 5.2,
            "steps": 6200,
            "calories": 320,
            "start_lat_lng": (37.7749, -122.4194),
            "end_lat_lng": (37.7849, -122.4294),
        }]
        result = self.app.run(workouts)
        self.assertIn("Workout 1:", result.output)
        self.assertIn("Distance: 5.2 mi", result.output)
        self.assertIn("Steps: 6200", result.output)
        self.assertIn("Calories Burned: 320", result.output)

    def test_multiple_workouts(self):
        """Tests displaying multiple workouts."""
        workouts = [
            {
                "start_time": " 08:00:00",
                "end_time": "08:30:00",
                "date": "2024-02-20",
                "workout_id": "workout1",
                "distance": 5.2,
                "steps": 6200,
                "calories": 320,
                "start_lat_lng": (37.7749, -122.4194),
                "end_lat_lng": (37.7849, -122.4294),
            },
            {
                "start_time": "09:00:00",
                "end_time": "09:45:00",
                "date": "2024-02-21",
                "workout_id": "workout2",
                "distance": 7.8,
                "steps": 8900,
                "calories": 450,
                "start_lat_lng": (40.7128, -74.0060),
                "end_lat_lng": (40.7328, -74.0160),
            },
        ]
        result = self.app.run(workouts)
        self.assertIn("Workout 1:", result.output)
        self.assertIn("Workout 2:", result.output)
        self.assertIn("Distance: 5.2 mi", result.output)
        self.assertIn("Distance: 7.8 mi", result.output)


if __name__ == "__main__":
    unittest.main()
