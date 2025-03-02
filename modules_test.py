#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def setUp(self):
        """Initialize AppTest before each test."""
        self.app = AppTest(display_recent_workouts)

    def test_no_workouts(self):
        """Tests if the function correctly handles an empty workout list."""
        self.app.run([])  # Simulating an empty workouts list
        self.assertIn("No recent workouts available.", self.app.html)

    def test_single_workout(self):
        """Tests displaying a single workout entry."""
        workout = [{
            "start_time": "2024-02-20 08:00:00",
            "end_time": "2024-02-20 08:30:00",
            "distance": 5.2,
            "steps": 6200,
            "calories": 320,
            "start_coords": (37.7749, -122.4194),
            "end_coords": (37.7849, -122.4294),
        }]
        self.app.run(workout)
        self.assertIn("Start Time: 2024-02-20 08:00:00", self.app.html)
        self.assertIn("Distance: 5.2 km", self.app.html)
        self.assertIn("Calories Burned: 320", self.app.html)

    def test_multiple_workouts(self):
        """Tests displaying multiple workout entries."""
        workouts = [
            {
                "start_time": "2024-02-20 08:00:00",
                "end_time": "2024-02-20 08:30:00",
                "distance": 5.2,
                "steps": 6200,
                "calories": 320,
                "start_coords": (37.7749, -122.4194),
                "end_coords": (37.7849, -122.4294),
            },
            {
                "start_time": "2024-02-21 09:00:00",
                "end_time": "2024-02-21 09:45:00",
                "distance": 7.8,
                "steps": 8900,
                "calories": 450,
                "start_coords": (40.7128, -74.0060),
                "end_coords": (40.7328, -74.0160),
            },
        ]
        self.app.run(workouts)
        self.assertIn("Start Time: 2024-02-20 08:00:00", self.app.html)
        self.assertIn("Start Time: 2024-02-21 09:00:00", self.app.html)
        self.assertIn("Distance: 7.8 km", self.app.html)
        self.assertIn("Calories Burned: 450", self.app.html)

if __name__ == "__main__":
    unittest.main()
