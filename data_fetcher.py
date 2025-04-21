import os
import streamlit as st
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel
from datetime import datetime
import hashlib
import numpy as np


PROJECT_ID = os.getenv("PROJECT_ID", "genial-venture-454302-f9")
DATASET_ID = "Three_Musketeers_Data"
client = bigquery.Client(project=PROJECT_ID)

# --- Auth Helpers ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    table_name = get_table_name("Users")
    hashed = hash_password(password)
    query = f"""
    SELECT * FROM `{table_name}`
    WHERE Username = '{username}' AND PasswordHash = '{hashed}'
    """
    results = run_query(query)
    return results[0] if results else None


def register_user(full_name, username, dob, image_url, password):
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{DATASET_ID}.Users"

    # Check if username already exists
    check_query = f"SELECT Username FROM `{table_id}` WHERE Username = '{username}'"
    existing = client.query(check_query).result()
    if existing.total_rows > 0:
        raise ValueError(f"Username '{username}' is already taken.")

    # Get all current UserIds
    query = f"SELECT UserId FROM `{table_id}`"
    results = client.query(query).result()
    user_ids = [row.UserId for row in results]

    # Extract numeric parts of user IDs
    numeric_ids = []
    for uid in user_ids:
        try:
            numeric_ids.append(int(uid.replace("user", "")))
        except:
            continue

    next_id = max(numeric_ids) + 1 if numeric_ids else 1
    new_user_id = f"user{next_id}"

    # Insert new user
    insert_query = f"""
    INSERT INTO `{table_id}` (UserId, Name, Username, ImageUrl, DateOfBirth, PasswordHash)
    VALUES (
        '{new_user_id}',
        '{full_name}',
        '{username}',
        '{image_url}',
        '{dob}',
        '{hash_password(password)}'
    )
    """
    client.query(insert_query).result()
    return new_user_id


def update_profile_image(user_id, new_url):
    table = get_table_name("Users")
    query = f"""
    UPDATE `{table}`
    SET ImageUrl = '{new_url}'
    WHERE UserId = '{user_id}'
    """
    client.query(query).result()

# --- General Helpers ---
def get_table_name(table_name):
    return f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

def run_query(query):
    query_job = client.query(query)
    return [dict(row) for row in query_job.result()]

# --- Data Retrieval ---
def get_user_sensor_data(user_id, workout_id):
    sensor_data_table = get_table_name("SensorData")
    sensor_type_table = get_table_name("SensorTypes")
    workout_table = get_table_name("Workouts")
    query = f"""
    SELECT sd.WorkoutID, sd.timestamp, sd.SensorValue, st.Name, st.Units
    FROM `{sensor_data_table}` sd
    JOIN `{sensor_type_table}` st ON sd.SensorId = st.SensorId
    JOIN `{workout_table}` w ON sd.WorkoutID = w.WorkoutId
    WHERE w.UserId = '{user_id}' AND sd.WorkoutID = '{workout_id}'
    ORDER BY sd.timestamp
    """
    return run_query(query)

def get_user_workouts(userid):
    table_name = get_table_name("Workouts")
    return run_query(f"SELECT * FROM `{table_name}` WHERE userId = '{userid}'")

def get_recent_workouts(userid):
    table_name = get_table_name("Workouts")
    return run_query(f"SELECT * FROM `{table_name}` WHERE userId = '{userid}' ORDER BY timestamp DESC LIMIT 3")

def get_genai_advice(userid):
    vertexai.init(project=PROJECT_ID)
    model = GenerativeModel("gemini-1.5-flash-002")
    workout = get_user_workouts(userid)
    if not workout:
        return {
            'advice': "No workout data available.",
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'image_url': "https://picsum.photos/200"
        }
    cals = workout[0].get('CaloriesBurned')
    prompt = f"You are a knowledgeable fitness motivator. The user burned {cals} calories. Motivate them!"
    response = model.generate_content(prompt)
    return {
        'advice': response.text,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'image_url': "https://picsum.photos/200"
    }

def get_user_profile(user_id):
    table_name = get_table_name("Users")
    user_data = run_query(f"SELECT * FROM `{table_name}` WHERE UserId = '{user_id}'")
    if not user_data:
        return None
    friends_table = get_table_name("Friends")
    friends_data = run_query(f"SELECT UserId2 FROM `{friends_table}` WHERE UserId1 = '{user_id}'")
    friends_list = [friend['UserId2'] for friend in friends_data]
    return {
        'full_name': user_data[0].get('Name', ''),
        'username': user_data[0].get('Username', ''),
        'date_of_birth': user_data[0].get('DateOfBirth', ''),
        'profile_image': user_data[0].get('ImageUrl', ''),
        'friends': friends_list
    }

def get_user_friends(user_id):
    table_name = get_table_name("Users")
    user_data = run_query(f"SELECT * FROM `{table_name}` WHERE UserId = '{user_id}'")
    if not user_data:
        return None
    friends_table = get_table_name("Friends")
    friends_data = run_query(f"SELECT UserId2 FROM `{friends_table}` WHERE UserId1 = '{user_id}'")
    friends_list = [friend['UserId2'] for friend in friends_data]
    friends_name = []
    for person in friends_list:
        table_name = get_table_name("Users")
        user_data = run_query(f"SELECT Name FROM `{table_name}` WHERE UserId = '{person}'")
        friends_name.append(user_data[0].get('Name', ''))

    return friends_name

def get_user_posts(user_id):
    table_name = get_table_name("Posts")
    return run_query(f"SELECT * FROM `{table_name}` WHERE AuthorId = '{user_id}' ORDER BY timestamp DESC")

def get_friends_post(author_ids):
    table_name = get_table_name("Posts")
    if not author_ids:
        return []
    formatted_ids = ", ".join(f"'{aid}'" for aid in author_ids)
    return run_query(
        f"SELECT * FROM `{table_name}` WHERE AuthorId IN ({formatted_ids}) ORDER BY timestamp DESC LIMIT 10"
    )


def insert_post(postId, author_id, timestamp, content, image_url):
    table_name = get_table_name("Posts")
    query = f"""
    INSERT INTO `{table_name}` (PostId, AuthorId, Timestamp, Content, ImageUrl)
    VALUES ('{postId}', '{author_id}', '{timestamp}', '{content}', '{image_url}')
    """
    try:
        client.query(query).result()
        return True
    except Exception as e:
        print(f"Insert error: {e}")
        return False

@st.cache_data(ttl=300)
def get_challenges():
    table_name = get_table_name("Challenges")
    return run_query(f"SELECT * FROM `{table_name}`")

@st.cache_data(ttl=300)
def get_challenge_details(challenge_id):
    table_name = get_table_name("ChallengeSteps")
    return run_query(f"SELECT * FROM `{table_name}` WHERE challenge_id = {challenge_id} ORDER BY step_number ASC")

def get_all_users():
    table_name = get_table_name("Users")
    return run_query(f"SELECT UserId, Name, Username, ImageUrl FROM `{table_name}` WHERE LENGTH(UserId) <= 6")
