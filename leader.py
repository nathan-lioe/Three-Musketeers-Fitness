import streamlit as st
import pandas as pd
from data_fetcher import get_all_users, get_user_workouts
from modules import display_leaderboard

def process_data():
    user_info = []
    users = get_all_users()
    for x in users:
        id = x.get("UserId")
        username = x.get("Username")
        image = x.get("ImageUrl")

        workouts = get_user_workouts(id)
        steps = workouts[0].get("TotalSteps")
        calories = workouts[0].get("CaloriesBurned")
        combined = (0.4 * steps) + (0.6 * calories)
        user_info.append([id, username, image, steps, calories, combined])
    return user_info
    
        
def show_leaderboard():
    rank = 1
    user_info = process_data()
    sorted_data = sorted(user_info, key=lambda x: x[-1],reverse=True)

    for x in sorted_data:
        display_leaderboard(rank, x[2], x[1], x[-1], x[3], x[4])
        rank += 1

def plot_steps_comparison():
    data = process_data()
    df = pd.DataFrame(data, columns=["UserId", "Username", "ImageUrl", "Steps", "Calories", "Combined"])
    
    steps_data = df.set_index("Username")["Calories"]
    
    # Display a bar chart comparing each person's steps.
    st.subheader("Calories burnt progress")
    st.bar_chart(steps_data)

import altair as alt

def plot_horizontal_barchart_altair():
    data = process_data()
    df = pd.DataFrame(data, columns=["UserId", "Username", "ImageUrl", "Steps", "Calories", "Combined"])

    st.subheader("Steps progress")
    chart = alt.Chart(df).mark_bar(color='teal').encode(
        x=alt.X('Steps:Q'),
        y=alt.Y('Username:N', sort='-x')  
    ).properties(
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)

def leader_components():
    st.header("Leaderboard & Progress")
    col1, col2 = st.columns([5, 5])

    with col1:
            st.subheader("Leaderboard")
            show_leaderboard()

    with col2:
        plot_horizontal_barchart_altair()
        plot_steps_comparison()
    





        






