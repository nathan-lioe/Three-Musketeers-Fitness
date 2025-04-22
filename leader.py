import streamlit as st
import pandas as pd
from data_fetcher import get_all_users, get_user_workouts, get_all_user_workouts
from modules import display_leaderboard
import altair as alt

def process_data():
    user_info = []
    users = get_all_users()
    user_ids = [x.get("UserId") for x in users]

    # Batch query for all workout totals
    workout_data = get_all_user_workouts(user_ids)

    workouts_by_user = {
        row["UserId"]: {
            "Steps": row.get("Steps", 0),
            "Calories": row.get("Calories", 0)
        }
        for row in workout_data
    }

    # Merge user info + computed score
    for x in users:
        uid = x.get("UserId")
        username = x.get("Username")
        image = x.get("ImageUrl")

        stats = workouts_by_user.get(uid, {"Steps": 0, "Calories": 0})
        steps = stats["Steps"]
        calories = stats["Calories"]
        combined = (0.4 * steps) + (0.6 * calories)
        user_info.append([uid, username, image, steps, calories, combined])

    return user_info

def show_leaderboard():
    st.subheader("Leaderboard")
    rank = 1
    user_info = process_data()
    sorted_data = sorted(user_info, key=lambda x: x[-1], reverse=True)

    for uid, username, image, steps, calories, combined in sorted_data:
        display_leaderboard(rank, image, username, combined, steps, calories)
        rank += 1

def plot_steps_comparison():
    data = process_data()
    df = pd.DataFrame(
        data,
        columns=["UserId", "Username", "ImageUrl", "Steps", "Calories", "Combined"]
    )
    # Compare calories 
    calories_data = df.set_index("Username")["Calories"]

    st.subheader("Calories Burned Progress")
    st.bar_chart(calories_data)

def plot_horizontal_barchart_altair():
    data = process_data()
    df = pd.DataFrame(
        data,
        columns=["UserId", "Username", "ImageUrl", "Steps", "Calories", "Combined"]
    )

    st.subheader("Steps Progress")
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("Steps:Q"),
            y=alt.Y("Username:N", sort="-x")
        )
        .properties(width=600, height=300)
    )
    st.altair_chart(chart, use_container_width=True)

def leader_components():
    st.header("Leaderboard & Progress")
    col1, col2 = st.columns(2)

    with col1:
        show_leaderboard()

    with col2:
        plot_horizontal_barchart_altair()
        plot_steps_comparison()
