import streamlit as st
from modules import display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_profile, get_user_sensor_data, get_user_workouts, get_genai_advice
from community import show_posts
from activity import display
from mood_playlists import get_mood, get_speed_category, embed_spotify_player, get_vertex_playlist, get_vertex_playlist_description, get_ai_spotify_playlist
from PIL import Image
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import numpy as np

# Set page config FIRST
st.set_page_config(layout="wide", page_title="Three Musketeers App")

# --- Custom CSS ---
st.markdown("""
<style>
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
    h1, h2, h3 {
        color: #1d4e69;
    }
    .stTabs [data-testid="stTabsContent"] {
        background-color: #f8f9fa;
        border-radius: 0 0 10px 10px;
        padding: 20px;
        border: 1px solid #e0e0e0;
        border-top: none;
    }
    .streamlit-expanderHeader {
        background-color: #e9ecef;
        color: #1d4e69;
        border-radius: 5px;
    }
    .stChart {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

userId = 'user1'

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["Activity", "Community", "Profile", "Music"])

# --- Activity Tab ---
with tab1:
    st.header("Activity Summary")
    display(userId)

# --- Community Tab ---
with tab2:
    st.title("Community Activity")
    col1, col2 = st.columns([6, 4])  
    with col1:
        show_posts(userId)
    with col2:
        advice = get_genai_advice(userId)
        display_genai_advice(advice.get("timestamp", ""), advice.get("advice", ""), advice.get("image_url", ""))

# --- Profile Tab ---
with tab3:
    st.title("Your Profile")
    col1, col2 = st.columns([1, 2])
    profile = get_user_profile(userId)
    user_profile = {
        "Name": profile.get("full_name", "Name"),
        "Username": profile.get("username", "Username"),
        "Date of Birth": profile.get("date_of_birth", "Date of Birth"),
        "Profile_Image": profile.get("profile_image", "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg")
    }
    with col1:
        st.image(user_profile.get("Profile_Image"), width=400)
    with col2:
        st.markdown("### Personal Information")
        st.write(f"**Name:** {user_profile.get('Name')}")
        st.write(f"**Username:** {user_profile.get('Username')}")
        st.write(f"**Date of Birth** {user_profile.get('Date of Birth')}")

# --- Music Tab ---
with tab4:
    st.markdown("""
        <style>
        .title-text {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1DB954;
            text-align: center;
        }
        .sub-text {
            text-align: center;
            font-size: 1.2rem;
            color: #555;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="title-text">MoodTunes 🎵</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Choose your vibe and we\'ll find the perfect playlist</p>', unsafe_allow_html=True)

    # Mood Cards
    mood_images = {
    "happy": "images/happy.png",
    "sad": "images/sad.png",
    "relaxed": "images/relaxed.png",
    "energetic": "images/energetic.png"
}

    # Initialize mood in session_state if not set
    if "selected_mood" not in st.session_state:
        st.session_state.selected_mood = "happy"

    # Mood selection buttons
    cols = st.columns(len(mood_images))
    for idx, (mood_name, img_url) in enumerate(mood_images.items()):
        with cols[idx]:
            st.image(img_url, width=100)
            if st.button(mood_name.capitalize()):
                st.session_state.selected_mood = mood_name

    # Use mood from session state
    mood = st.session_state.selected_mood

    # Energy Slider
    speed = st.slider("⚡ Pick your energy level:", min_value=1, max_value=10, value=5)
    speed_category = get_speed_category(speed)

    st.info(f"You're feeling **{mood.capitalize()}** with **{speed_category.capitalize()}** energy")

    # Lottie Animation (optional flair)
    def load_lottieurl(url: str):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        except:
            return None

    lottie_url = "https://assets3.lottiefiles.com/packages/lf20_tnlqocig.json"
    lottie_json = load_lottieurl(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=200)

    # Add a "Generate Playlists" button to trigger AI generation
    if st.button("Generate Playlists"):
        with st.spinner("AI is finding the perfect playlist for you..."):
            # Get AI-curated playlist description
            playlist_description = get_vertex_playlist_description(mood, speed_category)
            st.markdown(f"### 🎵 Your Mood Description")
            st.write(playlist_description)
            
            # Get AI-recommended Spotify playlist ID
            spotify_playlist_id = get_ai_spotify_playlist(mood, speed_category)
            
            # Display the playlist ID (for debugging/transparency)
            st.caption(f"Using Spotify playlist ID: {spotify_playlist_id}")
            
            # Embed the Spotify player
            st.markdown("### 🎧 Your AI-Selected Spotify Playlist")
            embed_spotify_player(spotify_playlist_id)
            
            # Generate AI custom playlist of songs
            ai_playlist = get_vertex_playlist(mood, speed_category)
            st.markdown("### 🧠 AI-Generated Song Recommendations")
            st.markdown(ai_playlist)