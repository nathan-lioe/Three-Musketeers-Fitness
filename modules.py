#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component



# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Write a good docstring here."""
    data ={
        'username' : username,
        'user_image' : user_image,
        'timestamp' : timestamp,
        'content' : content,
        'post_image' : post_image
    }

    html_file_name = "post"
    create_component(data, html_file_name, 600)


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
        # Get distance
        x_distance = x[0].get("distance", 0)
        total_distance += x_distance
        distance.append(x_distance)

        # Get total time worked out
        start_time = x[0].get("start_timestamp", "")
        end_time = x[0].get("end_timestamp", "")
        date.append(end_time[5:10])


        start_h, start_m = int(start_time[11:13]), int(start_time[14:16])
        end_h, end_m = int(end_time[11:13]), int(end_time[14:16])
        start_minutes = start_h * 60 + start_m
        end_minutes = end_h * 60 + end_m
        diff_minutes = end_minutes - start_minutes 
        total_minutes += diff_minutes
        time.append(diff_minutes)

        # Get calories burned
        x_calories = x[0].get("calories_burned", 0)
        total_calories += x_calories 
        calories.append(x_calories)
        # Get steps 
        x_steps = x[0].get("steps", 0)
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
    create_component(data, html_file_name,height=250)
    return date,steps, calories,distance,time


def format_date(timestamp_str):
    """Extracts the date (YYYY-MM-DD) from a timestamp string using slicing."""
    return timestamp_str[:10] if timestamp_str else "Unknown"

def format_time(timestamp_str):
    """Extracts the time (HH:MM:SS) from a timestamp string using slicing."""
    return timestamp_str[11:] if timestamp_str else "Unknown"


def display_recent_workouts(workouts_list):

    if not workouts_list:
        return None
        
    last_workout_info = None
    
    for workout in workouts_list:
        w_ID = workout.get('workout_id', 0)
        date = format_date(workout.get('start_timestamp', ""))
        start_time = format_time(workout.get('start_timestamp', ""))
        end_time = format_time(workout.get('end_timestamp', ""))
        start_lat = workout.get('start_lat_lng', 0)
        end_lat = workout.get('end_lat_lng', 0)
        distance = workout.get('distance', 0)
        steps = workout.get('steps', 0)
        calories = workout.get('calories_burned', 0)
        
        workout_data = {
            'WORKOUT_ID': w_ID,
            'DATE': date, 
            'START_TIME': start_time,  
            'END_TIME': end_time,
            'START_LAT_LNG': start_lat,
            'END_LAT_LNG': end_lat,
            'DISTANCE': distance,
            'STEPS': steps,
            'CALORIES_BURNED': calories
        }

        create_component(workout_data, "recent_workouts", height=600)
        
        last_workout_info = (w_ID, date, start_time, end_time, start_lat, end_lat, distance, steps, calories)
    
    return last_workout_info


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    data = {
        'timestamp' : timestamp,
        'content' : content,
        'post_image' : image
    }
    html_file_name = "gen_ai_display"
    create_component(data, html_file_name, 600)
