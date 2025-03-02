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
        # Create a Streamlit test app
        app_test = AppTest()
        
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
        
        # Run the function in the test app
        with app_test.container():
            display_recent_workouts(workouts)
        
        # Get the app snapshot
        app_test.run()
        
        # Check that the subheader exists with correct text
        subheader_elements = app_test.get_components("subheader")
        self.assertEqual(len(subheader_elements), 1)
        self.assertEqual(subheader_elements[0].value, "Recent Workouts")
        
        # Check that the expanders exist with correct titles
        expander_elements = app_test.get_components("expanderHeader")
        self.assertEqual(len(expander_elements), 2)
        self.assertIn(f"Workout 1 - {workouts[0]['start_time']}", expander_elements[0].label)
        self.assertIn(f"Workout 2 - {workouts[1]['start_time']}", expander_elements[1].label)
        
        # Check for text elements inside the expanders
        text_elements = app_test.get_components("markdown")
        
        # First workout details should be present
        self.assertTrue(any(f"**Start Time:** {workouts[0]['start_time']}" in element.value for element in text_elements))
        self.assertTrue(any(f"**End Time:** {workouts[0]['end_time']}" in element.value for element in text_elements))
        self.assertTrue(any(f"**Distance:** {workouts[0]['distance']} km" in element.value for element in text_elements))
        self.assertTrue(any(f"**Steps:** {workouts[0]['steps']}" in element.value for element in text_elements))
        self.assertTrue(any(f"**Calories Burned:** {workouts[0]['calories']}" in element.value for element in text_elements))
        self.assertTrue(any(f"**Start Coordinates:** {workouts[0]['start_coords']}" in element.value for element in text_elements))
        self.assertTrue(any(f"**End Coordinates:** {workouts[0]['end_coords']}" in element.value for element in text_elements))

    def test_display_recent_workouts_empty_list(self):
        # Create a Streamlit test app
        app_test = AppTest()
        
        # Run the function with empty list
        with app_test.container():
            display_recent_workouts([])
        
        # Get the app snapshot
        app_test.run()
        
        # Check that "No recent workouts available" message appears
        text_elements = app_test.get_components("markdown")
        self.assertTrue(any("No recent workouts available" in element.value for element in text_elements))
        
        # Check that the subheader is not present
        subheader_elements = app_test.get_components("subheader")
        self.assertEqual(len(subheader_elements), 0)

if __name__ == "__main__":
    unittest.main()
