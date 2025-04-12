#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_profile, get_user_sensor_data, get_user_workouts,get_genai_advice, get_challenges
from community import show_posts
from activity import display
import pandas as pd
import numpy as np
# import streamlit_extras.switch_page_button as spb  # For internal navigation

# Set page configuration with the dark blue background
st.set_page_config(layout="wide", page_title="Three Musketeers App")

# Add custom CSS for pill-style tabs
st.markdown("""
<style>
    /* Keep your custom tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1d4e69;
        border-radius: 30px;
        padding: 5px 10px;
        width: 100%;
        box-sizing: border-box;
        display: flex;
        gap: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        color: #e0e0e0;
        border: none;
        border-radius: 20px;
        padding: 8px 0;
        text-align: center;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0d2c3e;
        color: white;
    }
    
    /* Remove the white text color for normal content */
    /* h1, h2, h3, p {
        color: white;
    } */
    
    /* Instead, style headers with a color that complements your tabs */
    h1, h2, h3 {
        color: #1d4e69;
    }
    
    /* Add subtle styling for content areas to create visual hierarchy */
    .stTabs [data-testid="stTabsContent"] {
        background-color: #f8f9fa;
        border-radius: 0 0 10px 10px;
        padding: 20px;
        border: 1px solid #e0e0e0;
        border-top: none;
    }
    
    /* Add styling for expanders to match the theme */
    .streamlit-expanderHeader {
        background-color: #e9ecef;
        color: #1d4e69;
        border-radius: 5px;
    }
    
    /* Add a subtle accent border to charts */
    .stChart {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

userId = 'user1'

# Create a horizontal navigation menu with st.tabs
tab1, tab2, tab3, tab4 = st.tabs(["Activity", "Community", "Profile", "Leaderboard and Challenges"])

# Home tab
with tab1:

    st.header("Activity Summary")
    display(userId)

# Community tab
with tab2:
    st.title("Community Activity")
    col1, col2 = st.columns([6, 4])  
    with col1:
        show_posts(userId)
    with col2:
        advice= get_genai_advice(userId)
        display_genai_advice(advice.get("timestamp", ""), advice.get("advice", ""), advice.get("image_url", ""))
    

# Profile tab
with tab3:
    st.title("Your Profile")
    
    col1, col2 = st.columns([1, 2])
    profile = get_user_profile(userId)
    user_profile = {
        "Name": profile.get("full_name", "Name"),
        "Username": profile.get("username", "Username"),
        "Date of Birth": profile.get("date_of_birth", "Date of Birth"),
        "Profile_Image": profile.get("profile_image", " https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg ")

}
    
    with col1:
        #st.image(user_profile.get("Profile_Image"), width=400)
        st.image("https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg", width=400)
    
    with col2:
        up = user_profile.get('Name')
        user = user_profile.get("Username")
        dob = user_profile.get("Date of Birth")
        st.markdown("### Personal Information")
        st.write(f"**Name:** {up}")
        st.write(f"**Username:** {user}")
        st.write(f"**Date of Birth** {dob}")

with tab4:
    st.title("Leaderboard and Challenges")
    st.markdown("Weekly Challenges")
    challenges = get_challenges()
    
    for challenge in challenges:
        with st.container():
            st.subheader(challenge["challenge_name"])
            st.write(challenge["challenge_description"])
            # Convert ID to a string for use as a Streamlit key
            challenge_id_str = str(challenge["challenge_id"])
            if st.button(f"View Challenge: {challenge['challenge_name']}", key=challenge_id_str):
                st.session_state["selected_challenge"] = {
                    "id": challenge_id_str,
                    "name": challenge["challenge_name"],
                    "description": challenge["challenge_description"]
                }

                st.switch_page("pages/challenge_details.py")



    

