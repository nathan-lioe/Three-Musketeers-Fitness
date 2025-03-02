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
    
    def test_display_recent_workouts_with_data(self):
        # Create a simple test script for AppTest
        test_script = "app.py"  # This should point to your app file
        
        # Create a Streamlit test app with script path
        app_test = AppTest(test_script)
        
        # Sample workout data
        workouts = [
            {
                'start_time': '2023-01-01 10:00:00',
                'end_time': '2023-01-01 11:00:00',
                'distance': 5.2,
                'steps': 6500,
                'calories': 450,
                'start_coords': '40.7128,-74.0060',
                'end_coords': '40.7135,-74.0070'
            },
            {
                'start_time': '2023-01-02 15:30:00',
                'end_time': '2023-01-02 16:15:00',
                'distance': 3.8,
                'steps': 4800,
                'calories': 320,
                'start_coords': '40.7140,-74.0065',
                'end_coords': '40.7150,-74.0075'
            }
        ]
        
        # Call the function directly
        display_recent_workouts(workouts)
        
        # Verify the function doesn't raise exceptions
        self.assertTrue(True)

    def test_display_recent_workouts_empty_list(self):
        # Call the function with empty list
        display_recent_workouts([])
        
        # Verify the function doesn't raise exceptions
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
