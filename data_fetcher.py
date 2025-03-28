import os
from google.cloud import bigquery
import vertexai                                            
from vertexai.generative_models import GenerativeModel 
from datetime import datetime

# Create API client
client = bigquery.Client(os.getenv("PROJECT_ID"))
table_name = f"ise-w-genai.CIS4993.Workouts"

# Perform query
def run_query(query):
    query_job = client.query(query)
    # Convert to hashable list format, which allows the caching to work
    rows = [dict(row) for row in query_job.result()]
    return rows

rows = run_query(f"SELECT * FROM `{table_name}`")

def get_user_sensor_data(user_id, workout_id):
    sensor_data_table = "CIS4993.SensorData"
    sensor_type_table = "CIS4993.SensorTypes"
    workout_table = "CIS4993.Workouts"

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

    # print("Some sensory data:")
    # for row in rows:
    #     print(row["SensorValue"])  

    return rows  # Return data for further processing if needed


def get_user_workouts(userid):
    """Write a good docstring here."""
    table_name = f"ise-w-genai.CIS4993.Workouts"
    rows = run_query(f"SELECT * FROM `{table_name}` WHERE userId = '{userid}'")
    return rows

def get_recent_workouts(userid):
    """Write a good docstring here."""
    table_name = f"ise-w-genai.CIS4993.Workouts"
    rows = run_query(f"SELECT * FROM `{table_name}` WHERE userId = '{userid}' ORDER BY timestamp DESC LIMIT=3")
    return rows

def get_genai_advice(userid):
    """
    Generate personalized workout advice for a user using Vertex AI's Gemini model.
    
    This function retrieves a user's workout data, extracts the calories burned,
    and uses the Gemini model to generate customized advice with a timestamp
    and a motivational image.
    
    Args:
        userid (str): The unique identifier for the user
        
    Returns:
        dict: A dictionary containing three keys:
            - 'advice': The personalized workout advice text
            - 'timestamp': Current timestamp when advice was generated
            - 'image_url': URL to a motivational fitness image from Pexels
    """

    vertexai.init(location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-002")
    workout = get_user_workouts(userid)
    
    cals = workout[0].get('CaloriesBurned')
    prompt = (
    f"You are a knowledgeable fitness motivator give the user motivation they burnt {cals} please give a sentence not just good job "


)
    
    
    response = model.generate_content(prompt)
    
    
    # Parse the response text to extract the components
    response_text = response.text
    # Extract advice, timestamp and image URL using string parsing
    advice_parts = {}
    
    
    advice_parts['advice'] = response_text

        
    advice_parts['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        

    advice_parts['image_url'] = "https://picsum.photos/200"
    
    return advice_parts

def get_user_profile(user_id):
    """
    Retrieve profile information for a specific user.
    
    This function queries the database for user profile data and returns
    a dictionary containing personal information and social connections.
    
    Args:
        user_id (str): The unique identifier for the user
        
    Returns:
        dict: A dictionary containing user profile information with the keys:
            - 'full_name': The user's full name
            - 'username': The user's username
            - 'date_of_birth': The user's date of birth
            - 'profile_image': URL to the user's profile image
            - 'friends': A list of user IDs representing the user's friends
    """
    table_name = f"ise-w-genai.CIS4993.Users"
    user_data = run_query(f"SELECT * FROM `{table_name}` WHERE UserId = '{user_id}'")
    
    if not user_data:
        return None
    
    # Get the friends list from the Friends table
    friends_table = f"ise-w-genai.CIS4993.Friends"
    friends_data = run_query(f"SELECT UserId2 FROM `{friends_table}` WHERE UserId1 = '{user_id}'")
    
    # Extract friend IDs into a list
    friends_list = [friend['UserId2'] for friend in friends_data]
    
    # Construct the profile dictionary
    profile = {
        'full_name': user_data[0].get('Name', ''),  # Changed to match output requirement
        'username': user_data[0].get('Username', ''),
        'date_of_birth': user_data[0].get('DateOfBirth', ''),
        'profile_image': user_data[0].get('ImageUrl', ''),
        'friends': friends_list
    }
    
    return profile


def get_user_posts(user_id):
    table_name = f"ise-w-genai.CIS4993.Posts"
    posts = run_query(f"SELECT * FROM `{table_name}` WHERE AuthorId = '{user_id}' ORDER BY timestamp DESC")
    return posts


def get_friends_post(author_ids):
    table_name = f"ise-w-genai.CIS4993.Posts"
    formatted_ids = ", ".join(f"'{author_id}'" for author_id in author_ids)
    posts = run_query(f"SELECT * FROM `{table_name}` WHERE AuthorId IN ({formatted_ids}) ORDER BY timestamp DESC LIMIT 10")
    return posts

def insert_post(postId,author_id, timestamp, content, image_url):
    table_name = f"ise-w-genai.CIS4993.Posts"
    query = run_query(f"INSERT INTO `{table_name}` (PostId,AuthorId,Timestamp, Content, ImageUrl) VALUES ('{postId}','{author_id}','{timestamp}', '{content}', '{image_url}')")




