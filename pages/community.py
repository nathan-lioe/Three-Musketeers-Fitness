import streamlit as st

st.title("Community Page")
st.subheader("Welcome to the Community!")

# Example content
st.write("""
This is the community section where users can:
- Share feedback
- Ask questions
- Connect with others
""")

# Community interaction example
name = st.text_input("Enter your name:")
message = st.text_area("Share your thoughts:")
if st.button("Post"):
    st.success(f"Thanks for sharing, {name}!")
