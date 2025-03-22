#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_profile, get_user_sensor_data, get_user_workouts
import pandas as pd
import numpy as np
import streamlit_extras.switch_page_button as spb  # For internal navigation


userId = 'user1'

def display_app_page():
    """Displays the home page of the app."""
    st.title('Three Musketeers App!')

    if st.button("Go to Community Page"):
        spb.switch_page("community")

    st.header("Activity Summary")

    # Fetch and display recent workouts
    recent_workouts = get_user_workouts(userId)
    
    if recent_workouts:
        workouts_data = recent_workouts
        st.header("🏋️ Recent Workouts")
        with st.expander("View Recent Workouts"):
            for workout in workouts_data: # iterate each workout
                display_recent_workouts(workout) # call display_recent_workouts for each workout
    else:
        st.write("🚫 No recent workouts available.")
        return

    # Display post
    st.header("Community activity")
    username = "roary"
    user_image = "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg"
    timestamp = "01-01-1900"
    content = "This is a test"
    post_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Ludovic_and_Lauren_%288425515069%29.jpg/330px-Ludovic_and_Lauren_%288425515069%29.jpg"
    display_post(username, user_image, timestamp, content, post_image)


# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
