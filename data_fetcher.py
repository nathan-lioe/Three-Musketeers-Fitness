from google.cloud import bigquery
import vertexai                                            
from vertexai.generative_models import GenerativeModel 
from datetime import datetime

# Create API client
client = bigquery.Client(project="composite-snow-453203-f9", location='US')


# Perform query
def run_query(query):
    query_job = client.query(query)
    # Convert to hashable list format
    rows = [dict(row) for row in query_job.result()]
    return rows

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

def get_user_workouts(user_id):
    """Fetches and returns a list of workouts for the given user from BigQuery."""
    workout_table = "CIS4993.Workouts"

    query = f'''
    SELECT WorkoutId, StartTimeStamp, EndTimeStamp, TotalDistance, TotalSteps, CaloriesBurned, StartLocationLat, EndLocationLat, StartLocationLong, EndLocationLong
    FROM `{workout_table}`
    WHERE UserId = '{user_id}'
    ORDER BY StartTimeStamp DESC
    '''

    rows = run_query(query)
    for row in rows:
        # Convert StartTimeStamp and EndTimeStamp to strings in 'YYYY-MM-DDTHH:MM:SS' format
        if isinstance(row['StartTimeStamp'], datetime):
            row['StartTimeStamp'] = row['StartTimeStamp'].strftime('%Y-%m-%dT%H:%M:%S')
        if isinstance(row['EndTimeStamp'], datetime):
            row['EndTimeStamp'] = row['EndTimeStamp'].strftime('%Y-%m-%dT%H:%M:%S')
    return rows

def get_user_profile(user_id):
    """Fetches and returns the profile information of a given user from BigQuery."""
    user_table = "CIS4993.Users"

    query = f'''
    SELECT UserId, Name, Username, DateOfBirth, ImageUrl
    FROM `{user_table}`
    WHERE UserId = '{user_id}'
    '''

    rows = run_query(query)
    return rows[0] if rows else None

def get_user_posts(user_id):
    """Fetches and returns a list of posts by a given user from BigQuery."""
    post_table = "CIS4993.Posts"

    query = f'''
    SELECT PostId, AuthorId, Timestamp, Content, ImageUrl
    FROM `{post_table}`
    WHERE AuthorId = '{user_id}'
    ORDER BY Timestamp DESC
    '''

    return run_query(query)

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
    
    response = model.generate_content(
        f"Give the advice on his workout and with a timestamp and a motivational image. "
        f"The person burned {cals} calories. It does not need to be specific just short and simple. "
        f"Give me a link with a Pexels image. Return in this format: "
        f"ADVICE: [your advice text] TIMESTAMP: [current timestamp] IMAGE: [pexels image url]"
    )
    
    print(response.text)
    
    # Parse the response text to extract the components
    response_text = response.text
    
    # Extract advice, timestamp and image URL using string parsing
    advice_parts = {}
    
    if "ADVICE:" in response_text:
        advice_parts['advice'] = response_text.split("ADVICE:")[1].split("TIMESTAMP:")[0].strip()
    else:
        advice_parts['advice'] = "Great job on your workout!"
        
    if "TIMESTAMP:" in response_text:
        advice_parts['timestamp'] = response_text.split("TIMESTAMP:")[1].split("IMAGE:")[0].strip()
    else:
        from datetime import datetime
        advice_parts['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    if "IMAGE:" in response_text:
        advice_parts['image_url'] = response_text.split("IMAGE:")[1].strip()
    else:
        # Default to Pexels workout images instead of Unsplash
        advice_parts['image_url'] = "https://www.pexels.com/search/quote/"
    
    return advice_parts



# Example usage
# if __name__ == '__main__':
#     user_id = "user1"
#     workout_id = "workout1"
#     print(get_user_sensor_data(user_id, workout_id))
#     print(get_user_workouts(user_id))
#     print(get_user_profile(user_id))
#     print(get_user_posts(user_id))
    
