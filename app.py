import streamlit as st
from modules import display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_profile, get_user_sensor_data, get_user_workouts,  get_genai_advice, authenticate_user, register_user, get_challenges, get_challenge_details
from community import show_posts
from activity import display
from challenge import render_challenge_details
from leader import show_leaderboard
import datetime

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
        full_name = st.text_input("Full Name")
        reg_username = st.text_input("New Username")
        reg_password = st.text_input("New Password", type="password")
        dob = st.date_input(
        "Date of Birth",
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date(2025, 12, 30))

        if st.button("Register"):
            default_img = "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg"
            user_id = register_user(full_name, reg_username, dob.isoformat(), default_img, reg_password)
            st.success("Account created! You are now logged in.")
            st.session_state.user_id = user_id
            st.rerun()

    st.stop()

# --- If logged in, render main app ---
userId = st.session_state.user_id
tab1, tab2, tab3, tab4 = st.tabs(["Activity", "Community","Leaderboard and Challenges" ,"Profile"])

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

        
