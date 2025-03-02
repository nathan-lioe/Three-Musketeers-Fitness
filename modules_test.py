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
        """Initialize AppTest before each test with a required timeout."""
        self.app = AppTest(display_recent_workouts, default_timeout=10)

    def test_no_workouts(self):
        """Tests handling of an empty workout list."""
        self.app.run([])
        assert self.app.text == ["No recent workouts available."]

    def test_single_workout(self):
        """Tests displaying a single workout entry."""
        workouts = [{
            "start_time": "2024-02-20 08:00:00",
            "end_time": "2024-02-20 08:30:00",
            "distance": 5.2,
            "steps": 6200,
            "calories": 320,
            "start_coords": (37.7749, -122.4194),
            "end_coords": (37.7849, -122.4294),
        }]
        self.app.run(workouts)

        # Check if workout details are displayed correctly
        expected_text = [
            "Recent Workouts:",
            "Workout 1:",
            "Start Time: 2024-02-20 08:00:00",
            "End Time: 2024-02-20 08:30:00",
            "Distance: 5.2 km",
            "Steps: 6200",
            "Calories Burned: 320",
            "Start Coordinates: (37.7749, -122.4194)",
            "End Coordinates: (37.7849, -122.4294)",
        ]
        for text in expected_text:
            assert text in self.app.text, f"Expected '{text}' in output"

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

        # Check if multiple workouts are displayed
        assert "Workout 1:" in self.app.text
        assert "Workout 2:" in self.app.text

if __name__ == "__main__":
    unittest.main()
