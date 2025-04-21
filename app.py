import streamlit as st
from modules import display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_profile, get_user_sensor_data, get_user_workouts,  get_genai_advice, authenticate_user, register_user, get_challenges, get_challenge_details
from community import show_posts
from activity import display
from challenge import render_challenge_details
from leader import show_leaderboard
import datetime
from mood_playlists import get_mood, get_speed_category, embed_spotify_player, get_vertex_playlist, get_vertex_playlist_description, get_ai_spotify_playlist
from PIL import Image
from streamlit_lottie import st_lottie
import requests

# Streamlit setup
st.set_page_config(layout="wide", page_title="Three Musketeers App")

# Custom styles
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

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if "page" not in st.session_state:
    st.session_state["page"] = "home"


# --- Logout check and reset before anything else ---
if st.session_state.user_id is None:
    auth_tab, reg_tab = st.tabs(["🔐 Login", "📝 Register"])

    with auth_tab:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = authenticate_user(username, password)
            if user:
                st.session_state.user_id = user["UserId"]
                st.rerun()
            else:
                st.error("Invalid username or password")

        with reg_tab:
            st.subheader("Create an Account")
            full_name    = st.text_input("Full Name")
            reg_username = st.text_input("New Username")
            reg_password = st.text_input("New Password", type="password")
            dob = st.date_input(
                "Date of Birth",
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date(2025, 12, 30)
            )

            if st.button("Register"):
                default_img = "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg"
                try:
                    # This will raise ValueError if the username is taken
                    user_id = register_user(full_name, reg_username, dob.isoformat(), default_img, reg_password)
                    st.success("Account created! You are now logged in.")
                    st.session_state.user_id = user_id
                    st.rerun()
                except ValueError as e:
                    # Show the specific “username taken” message
                    st.error(f"{e} Please choose a different username and try again.")
                except Exception:
                    # Fallback for any other error
                    st.error("Registration failed unexpectedly. Please try again later.")


    st.stop()

# --- If logged in, render main app ---
userId = st.session_state.user_id
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Activity", "Community", "Leaderboard and Challenges", "Profile", "Music"])

if st.session_state["page"] == "challenge_details":
    render_challenge_details(st.session_state.get("selected_challenge"))
    st.stop()

with tab1:
    st.header("Activity Summary")
    display(userId)

    # Community Tab
    with tab2:
        st.header("Community Activity")
        col1, col2 = st.columns([6, 4])
        with col1:
            show_posts(userId)
        with col2:
            advice = get_genai_advice(userId)
            display_genai_advice(advice.get("timestamp", ""), advice.get("advice", ""), advice.get("image_url", ""))


        # Challenges Tab
        with tab3:
            st.header("Weekly Challenges")

            challenges = get_challenges()

            num_cols = 3  # Two challenges per row
            rows = [challenges[i:i+num_cols] for i in range(0, len(challenges), num_cols)]

            for row in rows:
                cols = st.columns(num_cols)
                for col, challenge in zip(cols, row):
                    with col:
                        challenge_id_str = str(challenge["challenge_id"])
                        
                        with st.container(border=True):  # Native bordered card
                            st.subheader(challenge["challenge_name"])
                            st.write(challenge["challenge_description"])

                            if st.button("View Challenge", key=challenge_id_str):
                                st.session_state["selected_challenge"] = {
                                    "id": challenge_id_str,
                                    "name": challenge["challenge_name"],
                                    "description": challenge["challenge_description"]
                                }
                                st.session_state["page"] = "challenge_details"
                                st.rerun()
            
            show_leaderboard()
            
            
        # Profile Tab
        with tab4:
            st.header("Your Profile")
            col1, col2 = st.columns([1, 2])
            profile = get_user_profile(userId)
            user_profile = {
                "Name": profile.get("full_name", "Name"),
                "Username": profile.get("username", "Username"),
                "Date of Birth": profile.get("date_of_birth", "Date of Birth"),
                "Profile_Image": profile.get("profile_image", "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg")
            }

            with col1:
                st.image(user_profile["Profile_Image"], width=400)

            with col2:
                st.markdown("### Personal Information")
                st.write(f"**Name:** {user_profile['Name']}")
                st.write(f"**Username:** {user_profile['Username']}")
                st.write(f"**Date of Birth:** {user_profile['Date of Birth']}")

                st.markdown("---")

                # Logout Button
                col_logout, col_switch = st.columns([1, 2])
                with col_logout:
                    if st.button("Logout of Account"):
                        st.session_state.user_id = None
                        st.session_state.page = "home"
                        st.success("You have been logged out.")
                        st.rerun()

                # Demo Switch Dropdown
                with col_switch:
                    demo_usernames = {
                        "Alice Johnson (user1)": "user1",
                        "Bob Smith (user2)": "user2",
                        "Charlie Brown (user3)": "user3"
                    }

                    selected_demo = st.selectbox("Switch Demo Account",list(demo_usernames.keys()))
                    if st.button("Switch Account"):
                        st.session_state.user_id = demo_usernames[selected_demo]
                        st.success(f"Switched to {selected_demo}")
                        st.rerun()

        # --- Music Tab ---
        with tab5:
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

                    # Two columns: Left for Spotify, Right for AI-generated playlist
                    col_left, col_right = st.columns(2)

                    with col_left:
                        st.markdown("### 🎧 Your AI-Selected Spotify Playlist")
                        embed_spotify_player(spotify_playlist_id)

                    with col_right:
                        st.markdown("### 🧠 AI-Generated Song Recommendations")
                        ai_playlist = get_vertex_playlist(mood, speed_category)
                        st.markdown(ai_playlist)

        
