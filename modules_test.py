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
        """Initialize AppTest before each test with required parameters."""
        self.app = AppTest(display_recent_workouts, default_timeout=10)

    def test_no_workouts(self):
        """Tests when there are no recent workouts."""
        result = self.app.run([])
        self.assertIn("No recent workouts available.", result.output)

    def test_single_workout(self):
        """Tests displaying a single workout."""
        workouts = [{
            "start_time": "2024-02-20 08:00:00",
            "end_time": "2024-02-20 08:30:00",
            "distance": 5.2,
            "steps": 6200,
            "calories": 320,
            "start_coords": (37.7749, -122.4194),
            "end_coords": (37.7849, -122.4294),
        }]
        result = self.app.run(workouts)
        self.assertIn("Workout 1:", result.output)
        self.assertIn("Distance: 5.2 km", result.output)
        self.assertIn("Steps: 6200", result.output)
        self.assertIn("Calories Burned: 320", result.output)

    def test_multiple_workouts(self):
        """Tests displaying multiple workouts."""
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
        result = self.app.run(workouts)
        self.assertIn("Workout 1:", result.output)
        self.assertIn("Workout 2:", result.output)
        self.assertIn("Distance: 5.2 km", result.output)
        self.assertIn("Distance: 7.8 km", result.output)

if __name__ == "__main__":
    unittest.main()
