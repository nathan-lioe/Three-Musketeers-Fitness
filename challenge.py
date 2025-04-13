import streamlit as st
from data_fetcher import get_challenge_details

def render_challenge_details(selected_challenge):
    if not selected_challenge:
        st.warning("No challenge selected. Please go back and choose a challenge.")
        return

    challenge_id = selected_challenge["id"]
    challenge_name = selected_challenge["name"]
    challenge_description = selected_challenge["description"]

    st.title(challenge_name)
    st.markdown(f"**Description:** {challenge_description}")
    st.markdown("### Challenge Steps:")

    challenge_steps = get_challenge_details(challenge_id)

    for step in challenge_steps:
        with st.expander(f"Step {step['step_number']}: {step['step_name']}"):
            st.write(step["step_description"])

    if st.button("🔙 Back to Challenges"):
        st.session_state["page"] = "home"
        st.rerun()