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
# For langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

userId = 'user1'


def display_app_page():
    """Displays the home page of the app."""
    st.title("Hello")

def display_summary_page():
    st.title("Activity Summary")
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
    st.header("Detailed workout list")
    st.table(table_data)
    st.markdown('#')

    st.header("Steps trend")
    chart_data = pd.DataFrame(
        {
            "Day": date,
            "Steps": steps
        }
    )
    st.bar_chart(chart_data, x="Day", y="Steps")

    load_dotenv()
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

    input = st.text_input("Any questions?")
    response = llm.invoke(input)
    st.write("Gemini's response:")
    st.write(response.content)


   

    
   
pg = st.navigation([
    st.Page(display_app_page, title="Home"),
    st.Page(display_summary_page, title="Activity Summary")
])
pg.run()


# This is the starting point for your app. You do not need to change these lines
# if __name__ == '__main__':
#     display_app_page()
