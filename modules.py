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
    pass


def display_activity_summary(workouts_list):
    """Write a good docstring here."""
    pass


def display_recent_workouts(workouts_list):
    def display_recent_workouts(workouts):
    """
    Displays a user's recent workouts.

    Args:
        workouts (list): A list of workout dictionaries. 
                         Each dictionary contains:
                         - 'start_time': str
                         - 'end_time': str
                         - 'distance': float
                         - 'steps': int
                         - 'calories': float
                         - 'start_coords': tuple(float, float)
                         - 'end_coords': tuple(float, float)

    Returns:
        None (Prints the formatted workout data)
    """
    if not workouts:
        print("No recent workouts available.")
        return

    print("\nRecent Workouts:")
    print("=" * 30)
    
    for i, workout in enumerate(workouts, 1):
        print(f"Workout {i}:")
        print(f"  Start Time: {workout['start_time']}")
        print(f"  End Time: {workout['end_time']}")
        print(f"  Distance: {workout['distance']} km")
        print(f"  Steps: {workout['steps']}")
        print(f"  Calories Burned: {workout['calories']}")
        print(f"  Start Coordinates: {workout['start_coords']}")
        print(f"  End Coordinates: {workout['end_coords']}")
        print("-" * 30)

    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
