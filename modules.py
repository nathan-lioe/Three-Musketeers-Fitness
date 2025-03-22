#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################
from internals import create_component

def display_activity_summary(workouts_list):
    """Write a good docstring here."""

    num_workouts = len(workouts_list)
    total_distance = 0
    total_steps = 0
    total_minutes = 0 
    total_calories = 0

    time = []
    steps = []
    date = []
    calories = []
    distance = []
    for x in workouts_list:

        x_distance = x.get("TotalDistance", 0)
        total_distance += x_distance
        distance.append(x_distance)

        #date
        start_time = x.get("StartTimestamp")
        end_time = x.get("EndTimestamp")
    
        # Check if timestamps exist
        if not start_time or not end_time:
            return 0, "Unknown date"
    
        # Calculate duration in minutes
        duration = end_time - start_time
        duration_minutes = duration.total_seconds() / 60
        time.append(duration_minutes)
        total_minutes += duration_minutes
        
        # 2. Extract just the date from start timestamp
        date_only = start_time.date()
        

        formatted_date = start_time.strftime("%Y-%m-%d")

        date.append(formatted_date)
        


        # Get calories burned
        x_calories = x.get("CaloriesBurned", 0)
        total_calories += x_calories 
        calories.append(x_calories)
        # Get steps 
        x_steps = x.get("TotalSteps", 0)
        total_steps += x_steps
        steps.append(x_steps)
    
    data = {
        'TOTAL_DISTANCE' : total_distance,
        'TOTAL_MINUTES' : total_minutes,
        'TOTAL_CALORIES': total_calories,
        'TOTAL_STEPS' : total_steps,
        'TOTAL_WORKOUTS': num_workouts,
        'TOTAL_TIME': total_minutes
    } 

    html_file_name = "display_summary"
    create_component(data, html_file_name,height=375)
    return date,steps, calories,distance,time



def display_genai_advice(advice_id, timestamp, content, image):
    """Write a good docstring here."""
    # data = {
    #     'timestamp' : timestamp,
    #     'content' : content,
    #     'post_image' : image
    # }
    # html_file_name = "gen_ai_display"
    # create_component(data, html_file_name, 600)
