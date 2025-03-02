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
        # Define a minimal test script function instead of a file path
        def test_script():
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
            display_recent_workouts(workouts)
        
        # Create AppTest with the function and required parameters
        app_test = AppTest(test_script, default_timeout=10)
        app_test.run()
        
        # Check that subheader exists with correct text
        subheaders = app_test.get("subheader")
        self.assertEqual(len(subheaders), 1)
        self.assertEqual(subheaders[0].value, "Recent Workouts")
        
        # Check that expanders exist
        expanders = app_test.get("expander")
        self.assertEqual(len(expanders), 2)
        
        # Check texts within the app for workout details
        markdowns = app_test.get("markdown")
        markdown_texts = [md.value for md in markdowns]
        
        # Check first workout details
        self.assertTrue(any("**Start Time:** 2023-01-01 10:00:00" in text for text in markdown_texts))
        self.assertTrue(any("**End Time:** 2023-01-01 11:00:00" in text for text in markdown_texts))
        self.assertTrue(any("**Distance:** 5.2 km" in text for text in markdown_texts))
        self.assertTrue(any("**Steps:** 6500" in text for text in markdown_texts))
        self.assertTrue(any("**Calories Burned:** 450" in text for text in markdown_texts))

    def test_display_recent_workouts_empty_list(self):
        # Define a minimal test script function for empty list
        def test_script():
            display_recent_workouts([])
        
        # Create AppTest with the function and required parameters
        app_test = AppTest(test_script, default_timeout=10)
        app_test.run()
        
        # Check for "No recent workouts available" message
        markdowns = app_test.get("markdown")
        markdown_texts = [md.value for md in markdowns]
        self.assertTrue(any("No recent workouts available" in text for text in markdown_texts))
        
        # Make sure no subheader is shown
        subheaders = app_test.get("subheader")
        self.assertEqual(len(subheaders), 0)

if __name__ == "__main__":
    unittest.main()
