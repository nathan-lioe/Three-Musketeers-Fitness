import streamlit as st
from modules import display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_profile, get_user_sensor_data, get_user_workouts,get_genai_advice, insert_post
from community import show_posts
from datetime import datetime
import pandas as pd
import numpy as np

def display(userId):
    workout_list = get_user_workouts(userId)
    date, steps, calories, distance, time = display_activity_summary(workout_list)

    steps_data = pd.DataFrame(
        {
            "Day": date,
            "Steps": steps
        }
    )

    recent_workouts = get_user_workouts(userId)
        
    if recent_workouts:
        workouts_data = recent_workouts
        st.header("🏋️ Recent Workouts")
        for workout in workouts_data: # iterate each workout
            display_recent_workouts(workout) # call display_recent_workouts for each workout
    else:
        st.write("🚫 No recent workouts available.")
        
    st.subheader("Daily Steps Trend")

    st.line_chart(
    steps_data.set_index("Day")["Steps"],  # This selects only the Steps column
    use_container_width=True  # This makes the chart use the full width
        )

    content = f"Look at this, I walked {steps[0]} steps today! #fitness #steps"
    if st.button("Share steps with community!"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        post_id = f"{userId}_{int(datetime.timestamp(datetime.now()))}"
        insert_post(post_id,userId,timestamp, content, "test")