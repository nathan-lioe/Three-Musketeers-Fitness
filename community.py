import streamlit as st
from data_fetcher import (
    get_user_profile,
    get_user_workouts,
    get_user_posts,
    get_friends_post,
    insert_post,
)
from modules import display_post
from datetime import datetime

def show_posts(uID):
    profile = get_user_profile(uID)
    friends = profile.get("friends", [])
    posts = get_friends_post(friends)
    username = profile.get("username", "")
    p_url = profile.get("ImageUrl", " ")

    # --- Handle input clearing ---
    if st.session_state.get("clear_post"):
        st.session_state.post_content = ""
        st.session_state.post_image_url = ""
        st.session_state.clear_post = False

    # --- Post Creation Section ---
    st.markdown(
        """
        <style>
        .post-creation-container {
            background-color: #f0f8ff;
            border: 2px solid #add8e6;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .post-creation-header {
            color: #1d4e69;
            font-size: 1.5em;
            margin-bottom: 10px;
            text-align: center;
        }
        .post-input {
            border: 1px solid #add8e6;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            outline: none;
        }
        .post-input:focus {
            border-color: #1d4e69;
            box-shadow: 0 0 5px rgba(29, 78, 105, 0.5);
        }
        .post-button {
            background-color: #1d4e69;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.3s;
            outline: none;
        }
        .post-button:hover {
            background-color: #0d2c3e;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<div class="post-creation-header">Share Your Thoughts!</div>', unsafe_allow_html=True)

        # Session state for user input
        if "post_content" not in st.session_state:
            st.session_state.post_content = ""
        if "post_image_url" not in st.session_state:
            st.session_state.post_image_url = ""

        post_content = st.text_area(
            "What's on your mind?",
            key="post_content",
            value=st.session_state.post_content,
            height=100,
            label_visibility="collapsed",
            placeholder="Write your post here...",
        )
        post_image_url = st.text_input(
            "Image URL (optional)",
            key="post_image_url",
            value=st.session_state.post_image_url,
            label_visibility="collapsed",
            placeholder="Enter image URL here...",
        )

        if st.button("Post", key="post_button"):
            if post_content:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                post_id = f"{uID}_{int(datetime.timestamp(datetime.now()))}"

                # Make sure argument order matches insert_post definition
                success = insert_post(post_id, uID, timestamp, post_content, post_image_url)

                if success is True:
                    st.success("Post created successfully!")
                    st.session_state.clear_post = True
                    st.rerun()
                elif isinstance(success, str):
                    st.error(f"Error creating post: {success}")
                else:
                    st.error("Failed to create post. Please try again.")
            else:
                st.warning("Please enter some text for your post.")

    # --- Display Posts Section ---
    st.subheader("Recent Posts")
    for x in posts:
        author_id = x.get("AuthorId", "")
        author_profile = get_user_profile(author_id)
        username = author_profile.get("username", "Unknown")
        user_image = author_profile.get("profile_image", "")
        timestamp = x.get("Timestamp", "")
        content = x.get("Content", "")
        post_image = x.get("ImageUrl", "")

        display_post(username, user_image, timestamp, content, post_image)
