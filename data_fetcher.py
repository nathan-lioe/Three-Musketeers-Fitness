import os
from google.cloud import bigquery
import vertexai                                            
from vertexai.generative_models import GenerativeModel 
from datetime import datetime

# --- Configuration ---
# Define the project ID and dataset ID as constants
PROJECT_ID = os.getenv("PROJECT_ID", "genial-venture-454302-f9")  # Default to the new project if not in env
DATASET_ID = "Three_Musketeers_Data"

# Create API client
client = bigquery.Client(project=PROJECT_ID)  # Specify the project ID here

# --- Helper Functions ---

def get_table_name(table_name):
    """Constructs the fully qualified table name."""
    return f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

# Perform query
def run_query(query):
    query_job = client.query(query)
    # Convert to hashable list format, which allows the caching to work
    rows = [dict(row) for row in query_job.result()]
    return rows

# --- Data Fetching Functions ---

def get_user_sensor_data(user_id, workout_id):
    sensor_data_table = get_table_name("SensorData")
    sensor_type_table = get_table_name("SensorTypes")
    workout_table = get_table_name("Workouts")

    query = f"""
    SELECT sd.WorkoutID, sd.timestamp, sd.SensorValue, st.Name, st.Units
    FROM `{sensor_data_table}` AS sd
    JOIN `{sensor_type_table}` AS st
    ON sd.SensorId = st.SensorId
    JOIN `{workout_table}` AS w
    ON sd.WorkoutID = w.WorkoutId
    WHERE w.UserId = '{user_id}' AND sd.WorkoutID = '{workout_id}'
    ORDER BY sd.timestamp
    """

    rows = run_query(query)
    return rows  

def get_user_workouts(userid):
    """Retrieves a user's workout data."""
    table_name = get_table_name("Workouts")
    rows = run_query(f"SELECT * FROM `{table_name}` WHERE userId = '{userid}'")
    return rows

def get_recent_workouts(userid):
    """Retrieves a user's most recent workouts."""
    table_name = get_table_name("Workouts")
    rows = run_query(f"SELECT * FROM `{table_name}` WHERE userId = '{userid}' ORDER BY timestamp DESC LIMIT 3")
    return rows

def get_genai_advice(userid):
    """
    Generates personalized workout advice for a user using Vertex AI's Gemini model.
    """
    vertexai.init(location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-002")
    workout = get_user_workouts(userid)
    
    if not workout:
        return {
            'advice': "No workout data available.",
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'image_url': "https://picsum.photos/200"
        }
    
    cals = workout[0].get('CaloriesBurned')
    prompt = (
    f"You are a knowledgeable fitness motivator give the user motivation they burnt {cals} please give a sentence not just good job "
    )
    
    response = model.generate_content(prompt)
    
    response_text = response.text
    advice_parts = {}
    
    advice_parts['advice'] = response_text
    advice_parts['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    advice_parts['image_url'] = "https://picsum.photos/200"
    
    return advice_parts

def get_user_profile(user_id):
    """Retrieves profile information for a specific user."""
    table_name = get_table_name("Users")
    user_data = run_query(f"SELECT * FROM `{table_name}` WHERE UserId = '{user_id}'")
    
    if not user_data:
        return None
    
    friends_table = get_table_name("Friends")
    friends_data = run_query(f"SELECT UserId2 FROM `{friends_table}` WHERE UserId1 = '{user_id}'")
    
    friends_list = [friend['UserId2'] for friend in friends_data]
    
    profile = {
        'full_name': user_data[0].get('Name', ''),
        'username': user_data[0].get('Username', ''),
        'date_of_birth': user_data[0].get('DateOfBirth', ''),
        'profile_image': user_data[0].get('ImageUrl', ''),
        'friends': friends_list
    }
    
    return profile

def get_user_posts(user_id):
    table_name = get_table_name("Posts")
    posts = run_query(f"SELECT * FROM `{table_name}` WHERE AuthorId = '{user_id}' ORDER BY timestamp DESC")
    return posts

def get_friends_post(author_ids):
    table_name = get_table_name("Posts")
    formatted_ids = ", ".join(f"'{author_id}'" for author_id in author_ids)
    posts = run_query(f"SELECT * FROM `{table_name}` WHERE AuthorId IN ({formatted_ids}) ORDER BY timestamp DESC LIMIT 10")
    return posts

def insert_post(postId,author_id, timestamp, content, image_url):
    table_name = get_table_name("Posts")
    #This is not a select query, so it should not be run_query
    query = f"INSERT INTO `{table_name}` (PostId,AuthorId,Timestamp, Content, ImageUrl) VALUES ('{postId}','{author_id}','{timestamp}', '{content}', '{image_url}')"
    client.query(query).result()
