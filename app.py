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



# Set page configuration with the dark blue background
st.set_page_config(layout="wide", page_title="Three Musketeers App")

# Add custom CSS for pill-style tabs
st.markdown("""
<style>
    

/* Make the tab container full width */

    .stTabs [data-baseweb="tab-list"] {
        background-color: #1d4e69;
        border-radius: 30px;
        padding: 5px 10px;
        width: 100%;        /* This makes it full width */
        box-sizing: border-box;
        display: flex;
        gap: 0;
    }
    
    /* Make tabs distribute evenly across the full width */
    .stTabs [data-baseweb="tab"] {
        flex: 1;            /* This makes each tab take equal space */
        color: #e0e0e0;
        border: none;
        border-radius: 20px;
        padding: 8px 0;     /* Vertical padding only, let flex handle width */
        text-align: center; /* Center the text in each tab */
        background-color: transparent;
    }
    /* Style the active tab */
    .stTabs [aria-selected="true"] {
        background-color: #0d2c3e;
        color: white;
    }
    
    /* Content area background (optional) */
    .stTabs [data-testid="stTabsContent"] {
        background-color: transparent;
        color: white;
    }
    
    /* Make headers and text white */
    h1, h2, h3, p {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

userId = 'user1'

# Create a horizontal navigation menu with st.tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Workouts", "Community", "Advice", "Profile"])

# Home tab
with tab1:

    st.header("Activity Summary")

    
    workout_list = get_user_workouts(userId)
    date, steps, calories, distance, time = display_activity_summary(workout_list)

    steps_data = pd.DataFrame(
    {
        "Day": date,
        "Steps": steps
    }
)


    st.subheader("Daily Steps Trend")

    st.line_chart(
    steps_data.set_index("Day")["Steps"],  # This selects only the Steps column
    use_container_width=True  # This makes the chart use the full width
    )
    




# Workouts tab
with tab2:
    st.title("Your Workouts")
    


# Community tab
with tab3:
    st.title("Community Activity")
    
    

# Advice tab
with tab4:
    st.title("AI Fitness Advice")
    

# Profile tab
with tab5:
    st.title("Your Profile")
    
    col1, col2 = st.columns([1, 2])
    
    # with col1:
    #     st.image("https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg", width=200)
    #     st.button("Update Photo")
    
    # with col2:
    #     st.text_input("Name", value="User One")
    #     st.number_input("Age", value=32)
    #     st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness"])
    #     st.number_input("Target Weekly Workouts", value=4)
    #     st.text_area("Bio", value="Fitness enthusiast trying to stay in shape!")
        
    # if st.button("Save Profile"):
    #     st.success("Profile updated successfully!")
    
    # # Settings section
    # st.header("Settings")
    # st.checkbox("Receive email notifications")
    # st.checkbox("Public profile")
    # st.select_slider("Privacy Level", options=["Low", "Medium", "High"])
def display_app_page():
    """Displays the home page of the app."""
    st.title('Three Musketeers App!')

    if st.button("Go to Community Page"):
        spb.switch_page("community")

    st.header("Activity Summary")

    
    workout_list = get_user_workouts(userId)
    date, steps, calories, distance, time = display_activity_summary(workout_list)

    steps_data = pd.DataFrame(
    {
        "Day": date,
        "Steps": steps
    }
)


    st.subheader("Daily Steps Trend")

    st.line_chart(
    steps_data.set_index("Day")["Steps"],  # This selects only the Steps column
    use_container_width=True  # This makes the chart use the full width
    )
    




# Workouts tab
with tab2:
    st.title("Your Workouts")
    


# Community tab
with tab3:
    st.title("Community Activity")
    
    

# Advice tab
with tab4:
    st.title("AI Fitness Advice")
    

# Profile tab
with tab5:
    st.title("Your Profile")
    
    col1, col2 = st.columns([1, 2])
    
    # with col1:
    #     st.image("https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg", width=200)
    #     st.button("Update Photo")
    
    # with col2:
    #     st.text_input("Name", value="User One")
    #     st.number_input("Age", value=32)
    #     st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness"])
    #     st.number_input("Target Weekly Workouts", value=4)
    #     st.text_area("Bio", value="Fitness enthusiast trying to stay in shape!")
        
    # if st.button("Save Profile"):
    #     st.success("Profile updated successfully!")
    
    # # Settings section
    # st.header("Settings")
    # st.checkbox("Receive email notifications")
    # st.checkbox("Public profile")
    # st.select_slider("Privacy Level", options=["Low", "Medium", "High"])