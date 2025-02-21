#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
import streamlit as st


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Write a good docstring here."""
    pass


def display_activity_summary(workouts_list):
    """Write a good docstring here."""
    pass


def display_recent_workouts(workouts_list):
   
    """
    Displays a user's recent workouts in a Streamlit app.

    Args:
        workouts_list (list): A list of workout dictionaries from `get_user_workouts()`.
    """
    if not workouts_list:
        st.write("No recent workouts available.")
        return

    st.subheader("Recent Workouts")

    for i, workout in enumerate(workouts_list, 1):
        with st.expander(f"Workout {i} - {workout['start_timestamp']}"):
            st.write(f"**Start Time:** {workout['start_timestamp']}")
            st.write(f"**End Time:** {workout['end_timestamp']}")
            st.write(f"**Distance:** {workout['distance']} km")
            st.write(f"**Steps:** {workout['steps']}")
            st.write(f"**Calories Burned:** {workout['calories_burned']}")
            st.write(f"**Start Coordinates:** {workout['start_lat_lng']}")
            st.write(f"**End Coordinates:** {workout['end_lat_lng']}")

    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
