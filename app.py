#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
import pandas as pd
import numpy as np

userId = 'user1'


def display_app_page():
    """Displays the home page of the app."""
    st.title('Three Musketeers App!')


    st.header("Activity Summary")

    # Test data
    list = []
    for x in range(3):
        test = get_user_workouts(userId)
        list.append(test)
    date, steps, calories,distance,time = display_activity_summary(list)
    table_data = pd.DataFrame(
        {
            "Day": date,
            "Calories": calories,
            "Steps": steps,
            "Distance": distance,
            "Time (minutes)": time
            
        }
    )
    st.subheader("Detailed workout list")
    st.table(table_data)
    st.markdown('#')

    st.subheader("Steps trend")
    chart_data = pd.DataFrame(
        {
            "Day": date,
            "Steps": steps
        }
    )
    st.bar_chart(chart_data, x="Day", y="Steps")

    # Fetch and display recent workouts
    recent_workouts = get_user_workouts(userId)

    if recent_workouts:
            st.header("🏋️ Recent Workouts")
            with st.expander("View Recent Workouts"):
                display_recent_workouts(recent_workouts)
    else:
        st.write("🚫 No recent workouts available.")
        return

    #display post
    st.header("Community activity")
    username = "roary"
    user_image = "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg"
    timestamp = "01-01-1900"
    content = "This is a test"
    post_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Ludovic_and_Lauren_%288425515069%29.jpg/330px-Ludovic_and_Lauren_%288425515069%29.jpg"
    display_post(username, user_image, timestamp, content, post_image)

    st.header("GenAi's advice")
    advice = get_genai_advice(userId)

    display_genai_advice(advice.get('timestamp'), advice.get('content'), advice.get('image'))

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()