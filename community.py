import streamlit as st
from data_fetcher import get_user_profile, get_user_workouts,get_user_posts, get_friends_post
from modules import display_post

def show_posts(uID):
    profile = get_user_profile(uID)
    p_url = profile.get("ImageUrl", " ")
    friends = profile.get("friends", [])
    posts = get_friends_post(friends)
    username = profile.get("username", "")

    for x in posts:
        profile = get_user_profile(x.get("AuthorId"," "))
        username = profile.get("username"," ")
        user_image = x.get("p_url"," ")
        timestamp = x.get("Timestamp"," ")
        content = x.get("Content"," ")
        post_image = x.get("ImageUrl"," ")
        display_post(username, user_image, timestamp, content, post_image)


    
