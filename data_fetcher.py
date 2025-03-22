#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# You will re-write these functions in Unit 3, and are welcome to alter the
# data returned in the meantime. We will replace this file with other data when
# testing earlier units.
#############################################################################
import os
from google.cloud import bigquery
import vertexai                                            
from vertexai.generative_models import GenerativeModel 



# Create API client
client = bigquery.Client()
table_name = f"ise-w-genai.CIS4993.Workouts"

# Perform query
def run_query(query):
    query_job = client.query(query)
    # Convert to hashable list format, which allows the caching to work
    rows = [dict(row) for row in query_job.result()]
    return rows

rows = run_query(f"SELECT * FROM `{table_name}`")


def get_user_workouts(userid):
    """Write a good docstring here."""
    table_name = f"ise-w-genai.CIS4993.Workouts"
    rows = run_query(f"SELECT * FROM `{table_name}` WHERE userId = '{userid}'")
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


listy = get_user_workouts("user1")

print(listy[1])

for x in listy:
    print(x)

