#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################
from internals import create_component
import pydeck as pdk
import streamlit as st
import pandas as pd
import numpy as np

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
        'TOTAL_DISTANCE' : round(total_distance,1),
        'TOTAL_MINUTES' : total_minutes,
        'TOTAL_CALORIES': total_calories,
        'TOTAL_STEPS' : total_steps,
        'TOTAL_WORKOUTS': num_workouts,
        'TOTAL_TIME': total_minutes
    } 

    html_file_name = "display_summary"
    create_component(data, html_file_name,height=375)
    return date,steps, calories,distance,time

def format_time(timestamp):
    """Extracts the time component from a timestamp, handling both datetime objects and strings."""
    if not timestamp:
        return "Unknown"
    
    # If it's a datetime object
    if hasattr(timestamp, 'strftime'):
        return timestamp.strftime('%H:%M:%S')
    
    # If it's a string
    return timestamp[11:19]  # Limiting to HH:MM:SS format

def display_map_for_workout(start_lat, start_lng, end_lat, end_lng):
    # Create detailed point data
    point_data = pd.DataFrame([
        {
            "lat": start_lat,
            "lon": start_lng,
            "label": "Start",
            "tooltip_text": f"Start of Workout::\n({start_lat:.4f}, {start_lng:.4f})"
        },
        {
            "lat": end_lat,
            "lon": end_lng,
            "label": "End",
            "tooltip_text": f"End of Workout:\n({end_lat:.4f}, {end_lng:.4f})"
        }
    ])

    # Point markers (start & end)
    layer_points = pdk.Layer(
        "ScatterplotLayer",
        data=point_data,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160]',
        get_radius=50,
        pickable=True  # Required for tooltips
    )

    # Line connecting start and end
    layer_line = pdk.Layer(
        "LineLayer",
        data=pd.DataFrame([{
            "start": [start_lng, start_lat],
            "end": [end_lng, end_lat]
        }]),
        get_source_position="start",
        get_target_position="end",
        get_color='[0, 100, 255]',
        get_width=3
    )

    # Center view between start and end
    midpoint = [(start_lat + end_lat) / 2, (start_lng + end_lng) / 2]

    view_state = pdk.ViewState(
        latitude=midpoint[0],
        longitude=midpoint[1],
        zoom=12,
        pitch=0
    )

    # Display the map with full tooltip info
    r = pdk.Deck(
        layers=[layer_points, layer_line],
        initial_view_state=view_state,
        tooltip={"text": "{tooltip_text}"}
    )

    st.pydeck_chart(r)



def display_recent_workouts(workout):
    """
    Format a single workout record and create a component to display it.

    Args:
        workout: A dictionary containing workout data
    """
    w_ID = workout.get('WorkoutId', 0)

    # Get the timestamp values
    start_timestamp = workout.get('StartTimestamp', "")
    end_timestamp = workout.get('EndTimestamp', "")

    # Format date and time separately
    date = start_timestamp
    start_time = format_time(start_timestamp)
    end_time = format_time(end_timestamp)

    start_lat = workout.get('StartLocationLat', 0)
    end_lat = workout.get('EndLocationLat', 0)
    start_lng = workout.get('StartLocationLong', 0)
    end_lng = workout.get('EndLocationLong', 0)
    distance = workout.get('TotalDistance', 0)
    steps = workout.get('TotalSteps', 0)
    calories = workout.get('CaloriesBurned', 0)

    workout_data = {
        'WORKOUT_ID': w_ID,
        'DATE': date,
        'START_TIME': start_time,
        'END_TIME': end_time,
        'START_LAT': start_lat,
        'START_LNG': start_lng,
        'END_LAT': end_lat,
        'END_LNG': end_lng,
        'DISTANCE': distance,
        'STEPS': steps,
        'CALORIES_BURNED': calories
    }

    create_component(workout_data, "recent_workouts", height=400)

    #map in expander
    with st.expander(f"Map of distance trecked for {w_ID}"):
        display_map_for_workout(start_lat, start_lng, end_lat, end_lng)



def display_genai_advice(timestamp, advice, image):
    """Write a good docstring here."""
    data = {
        'timestamp' : timestamp,
        'advice' : advice,
        'image' : image
    }
    html_file_name = "display_advice"
    create_component(data, html_file_name, 600)

def display_post(username, user_image, timestamp, content, post_image):
    data = {
        'username' : username,
        'user_image' : user_image,
        'timestamp' : timestamp,
        'content' : content,
        'post_image' : post_image
    }
    html_file_name = "display_post"
    create_component(data, html_file_name, 600)

def display_leaderboard(rank, picture, name, combined, steps, cals):
    data = {
        'rank' : rank,
        'picture' : picture,
        'name' : name,
        'combined' : combined,
        'steps' : steps,
        'cals' : cals
    }
    html_file_name = "leader_component"
    create_component(data, html_file_name, 160)
    
