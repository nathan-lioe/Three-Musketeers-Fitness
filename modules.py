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


def format_date(timestamp_str):
    """Extracts the date (YYYY-MM-DD) from a timestamp string using slicing."""
    return timestamp_str[:10] if timestamp_str else "Unknown"

def format_time(timestamp_str):
    """Extracts the time (HH:MM:SS) from a timestamp string using slicing."""
    return timestamp_str[11:] if timestamp_str else "Unknown"


def display_recent_workouts(workout): # changed this to only get one workout, and not a list of workouts
    
    w_ID = workout.get('WorkoutId', 0) # changed the capitalisation of this to be the same as in the data fetcher
    date = format_date(workout.get('StartTimeStamp', "")) # changed this to StartTimeStamp
    start_time = format_time(workout.get('StartTimeStamp', "")) # changed this to StartTimeStamp
    end_time = format_time(workout.get('EndTimeStamp', "")) # changed this to EndTimeStamp
    start_lat = workout.get('StartLocationLat', 0)
    end_lat = workout.get('EndLocationLat', 0)
    start_lng = workout.get('StartLocationLong', 0)
    end_lng = workout.get('EndLocationLong', 0)
    distance = workout.get('TotalDistance', 0) #changed this to TotalDistance
    steps = workout.get('TotalSteps', 0) #changed this to TotalSteps
    calories = workout.get('CaloriesBurned', 0) #changed this to CaloriesBurned
        
    workout_data = {
        'WORKOUT_ID': w_ID,
        'DATE': date, 
        'START_TIME': start_time,  
        'END_TIME': end_time,
        'START_LAT': start_lat,
        'START_LNG': start_lng,
        'END_LAT':end_lat,
        'END_LNG':end_lng,
        'DISTANCE': distance,
        'STEPS': steps,
        'CALORIES_BURNED': calories
    }

    create_component(workout_data, "recent_workouts", height=600)
    


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    # data = {
    #     'timestamp' : timestamp,
    #     'content' : content,
    #     'post_image' : image
    # }
    # html_file_name = "gen_ai_display"
    # create_component(data, html_file_name, 600)

def display_post():
    pass

def display_recent_workouts():
    pass
