import streamlit as st
from data_fetcher import get_challenge_details

# Get challenge info
selected_challenge = st.session_state.get("selected_challenge")

if not selected_challenge:
    st.warning("No challenge selected. Please go back and choose a challenge.")
    st.stop()

challenge_id = selected_challenge["id"]
challenge_name = selected_challenge["name"]
challenge_description = selected_challenge["description"]

# Page header
st.title(challenge_name)
st.markdown(f"**Description:** {challenge_description}")
st.markdown("### Challenge Steps:")

# Get step data (should return a list of step dicts from BigQuery)
challenge_steps = get_challenge_details(challenge_id)

# Display steps as expandable cards
for step in challenge_steps:
    with st.expander(f"Step {step['step_number']}: {step['step_name']}"):
        st.write(step["step_description"])

# Navigation back
if st.button("Back to Challenges"):
    st.switch_page("app.py")
