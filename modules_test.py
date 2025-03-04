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

    def test_foo(self):
        """Tests foo."""
        pass


if __name__ == "__main__":
    unittest.main()
