import streamlit as st
import datetime
from data_fetcher import get_user_workouts, get_user_profile, insert_post, run_query

# Set page configuration
st.set_page_config(page_title="Activity", layout="wide")

# Add custom CSS for styling (optional)
st.markdown("""
<style>
    h1, h2, h3, p {
        color: black;
    }
    .st-emotion-cache-6qob1r {
        background-color: #f0f0f5;
        border-radius: 30px;
    }
    .st-emotion-cache-10trblm {
        background-color: #f0f0f5c;
        border-radius: 30px;
    }
    .st-emotion-cache-1wrcr25 {
        background-color: #0d2c3e;
    }
</style>
""", unsafe_allow_html=True)

# Utility function for formatting date and time
def format_timestamp(timestamp):
    # Check if timestamp is already a datetime object
    if isinstance(timestamp, datetime.datetime):
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
    # Otherwise, parse it as a string
    return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

# Streamlit page setup
st.title("User Activity Page")

# Sidebar - Select user
user_id = st.sidebar.text_input("Enter User ID", "user1")

# Display user profile
profile = get_user_profile(user_id)
if profile:
    #st.sidebar.image(profile['ImageUrl'], width=100)
    st.sidebar.write(f"**{profile['Name']}**")
    st.sidebar.write(f"Username: {profile['Username']}")
    st.sidebar.write(f"Date of Birth: {profile['DateOfBirth']}")
else:
    st.sidebar.error("User not found")

# Display recent 3 workouts
st.subheader("Recent Workouts")
workouts = get_user_workouts(user_id)

# Debug: Print the entire workouts list
#st.write("Debug - All Workouts:", workouts)

if workouts:
    recent_workouts = workouts[:3]  # Display only the most recent 3 workouts
    for idx, workout in enumerate(recent_workouts):
        with st.expander(f"Workout {idx + 1} - {format_timestamp(workout['StartTimeStamp'])}"):
            st.write(f"**Workout ID:** {workout['WorkoutId']}")
            st.write(f"**Start:** {format_timestamp(workout['StartTimeStamp'])}")
            st.write(f"**End:** {format_timestamp(workout['EndTimeStamp'])}")
            st.write(f"**Distance:** {workout['TotalDistance']} km")
            st.write(f"**Steps:** {workout['TotalSteps']}")
            st.write(f"**Calories Burned:** {workout['CaloriesBurned']} kcal")


# Activity summary
st.subheader("Activity Summary")

if workouts:
    total_distance = sum(workout['TotalDistance'] for workout in workouts)
    total_steps = sum(workout['TotalSteps'] for workout in workouts)
    total_calories = sum(workout['CaloriesBurned'] for workout in workouts)

    st.write(f"**Total Distance:** {total_distance} km")
    st.write(f"**Total Steps:** {total_steps}")
    st.write(f"**Total Calories Burned:** {total_calories} kcal")
else:
    st.info("No workouts recorded.")

# Share button for posting a workout statistic
st.subheader("Share a Statistic with the Community")

# Initialize session state variables if they don't exist
if "preview_content" not in st.session_state:
    st.session_state.preview_content = ""

if workouts:
    # User can choose a workout statistic to share
    share_option = st.selectbox("Select a statistic to share", ["Steps", "Distance", "Calories Burned"])

    # Button to generate preview content
    if st.button("Generate Preview", key="generate_preview"):
        latest_workout = workouts[0]  # Use the most recent workout for preview

        if share_option == "Steps":
            st.session_state.preview_content = f"Look at this, I walked {latest_workout['TotalSteps']} steps today!"
        elif share_option == "Distance":
            st.session_state.preview_content = f"Look at this, I ran {latest_workout['TotalDistance']} km today!"
        elif share_option == "Calories Burned":
            st.session_state.preview_content = f"Look at this, I burned {latest_workout['CaloriesBurned']} kcal today!"

    # Display the preview content only if generated
    if st.session_state.preview_content:
        st.info(f"**Post Preview:** {st.session_state.preview_content}")
    else:
        st.warning("Click 'Generate Preview' to see your post preview.")

    # Share button with unique key
    if st.button("Share", key=f"share_{user_id}"):
        if st.session_state.preview_content:
            # Insert the post into the database
            insert_post(user_id, st.session_state.preview_content, image_url=None)

            # Clear the preview content after sharing
            st.session_state.preview_content = ""

            st.success("Your statistic has been shared with the community!")
        else:
            st.error("No preview generated. Click 'Generate Preview' first.")
