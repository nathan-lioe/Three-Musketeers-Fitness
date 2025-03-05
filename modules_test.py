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
        

        mock_create_component.assert_called_once_with(expected_data, "display_summary", height=250)
        

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
    
    @patch("modules.create_component")
    def test_no_workouts(self, mock_create_component):
        """Tests when there are no recent workouts."""

        result = display_recent_workouts([])
        
        mock_create_component.assert_not_called()
        
        self.assertIsNone(result)
    
    @patch("modules.create_component")
    def test_single_workout(self, mock_create_component):
        """Tests displaying a single workout."""
        workout = {
            "start_timestamp": "2024-02-19T08:00:00",
            "end_timestamp": "2024-02-19T08:30:00",
            "workout_id": "workout0",
            "distance": 5.2,
            "steps": 6200,
            "calories_burned": 320,
            "start_lat_lng": (37.7749, -122.4194),
            "end_lat_lng": (37.7849, -122.4294),
        }
        

        result = display_recent_workouts([workout])
        

        w_ID, date, start_time, end_time, start_lat, end_lat, distance, steps, calories = result

        self.assertEqual(w_ID, "workout0")

        self.assertEqual(start_lat, (37.7749, -122.4194))
        self.assertEqual(end_lat, (37.7849, -122.4294))
        self.assertEqual(distance, 5.2)
        self.assertEqual(steps, 6200)
        self.assertEqual(calories, 320)

        expected_data = {
            'WORKOUT_ID': 'workout0',
            'DATE': date,  
            'START_TIME': start_time,  
            'END_TIME': end_time,  
            'START_LAT_LNG': (37.7749, -122.4194),
            'END_LAT_LNG': (37.7849, -122.4294),
            'DISTANCE': 5.2,
            'STEPS': 6200,
            'CALORIES_BURNED': 320,
        }
        mock_create_component.assert_called_once_with(expected_data, 'recent_workouts', height=600)
    
    @patch("modules.create_component")
    def test_multiple_workouts(self, mock_create_component):
        """Tests displaying multiple workouts."""
        workouts = [
            {
                "start_timestamp": "2024-02-20T08:00:00",
                "end_timestamp": "2024-02-20T08:30:00",
                "workout_id": "workout1",
                "distance": 5.2,
                "steps": 6200,
                "calories_burned": 320,
                "start_lat_lng": (37.7749, -122.4194),
                "end_lat_lng": (37.7849, -122.4294),
            },
            {
                "start_timestamp": "2024-02-21T09:00:00",
                "end_timestamp": "2024-02-21T09:45:00",
                "workout_id": "workout2",
                "distance": 7.8,
                "steps": 8900,
                "calories_burned": 450,
                "start_lat_lng": (40.7128, -74.0060),
                "end_lat_lng": (40.7328, -74.0160),
            },
        ]
        

        result = display_recent_workouts(workouts)
        

        w_ID, date, start_time, end_time, start_lat, end_lat, distance, steps, calories = result
        

        self.assertEqual(w_ID, "workout2")
        self.assertEqual(date, "2024-02-21") 
        self.assertEqual(start_time, "09:00:00")  
        self.assertEqual(end_time, "09:45:00")
        self.assertEqual(start_lat, (40.7128, -74.0060))
        self.assertEqual(end_lat, (40.7328, -74.0160))
        self.assertEqual(distance, 7.8)
        self.assertEqual(steps, 8900)
        self.assertEqual(calories, 450)
        

        self.assertEqual(mock_create_component.call_count, 2)

        first_call_args = {
            'WORKOUT_ID': 'workout1',
            'DATE': '2024-02-20',  
            'START_TIME': '08:00:00', 
            'END_TIME': '08:30:00',
            'START_LAT_LNG': (37.7749, -122.4194),
            'END_LAT_LNG': (37.7849, -122.4294),
            'DISTANCE': 5.2,
            'STEPS': 6200,
            'CALORIES_BURNED': 320,
        }
        

        second_call_args = {
            'WORKOUT_ID': 'workout2',
            'DATE': '2024-02-21',
            'START_TIME': '09:00:00',
            'END_TIME': '09:45:00',
            'START_LAT_LNG': (40.7128, -74.0060),
            'END_LAT_LNG': (40.7328, -74.0160),
            'DISTANCE': 7.8,
            'STEPS': 8900,
            'CALORIES_BURNED': 450,
        }
        

        mock_create_component.assert_any_call(first_call_args, 'recent_workouts', height=600)
        mock_create_component.assert_any_call(second_call_args, 'recent_workouts', height=600)

if __name__ == "__main__":
    unittest.main()