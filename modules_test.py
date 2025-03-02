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
    
    def test_no_workouts(self):
        """Tests when there are no recent workouts."""
        # Create a test script for empty workouts
        def test_script():
            display_recent_workouts([])
            
        # Create a new AppTest instance for this test
        app = AppTest(test_script, default_timeout=10)
        app.run()
        
        # Check for "No recent workouts available" message
        markdown_elements = app.get("markdown")
        markdown_values = [element.value for element in markdown_elements]
        self.assertTrue(any("No recent workouts available" in value for value in markdown_values))
    
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
        
        # Create a test script for a single workout
        def test_script():
            display_recent_workouts(workouts)
            
        # Create a new AppTest instance for this test
        app = AppTest(test_script, default_timeout=10)
        app.run()
        
        # Check for expected elements
        markdown_elements = app.get("markdown")
        markdown_values = [element.value for element in markdown_elements]
        
        # Verify workout details are displayed
        self.assertTrue(any("**Distance:** 5.2 km" in value for value in markdown_values))
        self.assertTrue(any("**Steps:** 6200" in value for value in markdown_values))
        self.assertTrue(any("**Calories Burned:** 320" in value for value in markdown_values))
    
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
        
        # Create a test script for multiple workouts
        def test_script():
            display_recent_workouts(workouts)
            
        # Create a new AppTest instance for this test
        app = AppTest(test_script, default_timeout=10)
        app.run()
        
        # Check for expected elements
        expander_elements = app.get("expander")
        
        # Verify there are two expanders (one for each workout)
        self.assertEqual(len(expander_elements), 2)
        
        # Check for workout details in markdown elements
        markdown_elements = app.get("markdown")
        markdown_values = [element.value for element in markdown_elements]
        
        # Verify both workouts' details are displayed
        self.assertTrue(any("**Distance:** 5.2 km" in value for value in markdown_values))
        self.assertTrue(any("**Distance:** 7.8 km" in value for value in markdown_values))
        self.assertTrue(any("**Steps:** 6200" in value for value in markdown_values))
        self.assertTrue(any("**Steps:** 8900" in value for value in markdown_values))

if __name__ == "__main__":
    unittest.main()
