import os
import time
import streamlit as st
from openai import OpenAI
import boto3
from datetime import datetime
import csv
import re

# It also does not render equations in latex.
assistant_id    = st.secrets["assistant_id"]
st.image('https://www.physicslens.com/wp-content/uploads/2024/07/newtonslaws.png', caption="All about Newton's Laws of Motion!", width=480)
# Set openAi client , assistant ai and assistant ai thread
@st.cache_resource
def load_openai_client_and_assistant():
    client          = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    my_assistant    = client.beta.assistants.retrieve(st.secrets['assistant_id'])
    thread          = client.beta.threads.create()

    return client , my_assistant, thread

client,  my_assistant, assistant_thread = load_openai_client_and_assistant()

# check in loop  if assistant ai parse our request
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# initiate assistant ai response
def get_assistant_response(user_input=""):

    message = client.beta.threads.messages.create(
        thread_id=assistant_thread.id,
        role="user",
        content=user_input,
    )

    run = client.beta.threads.runs.create(
        thread_id=assistant_thread.id,
        assistant_id=assistant_id,
    )

    run = wait_on_run(run, assistant_thread)

    # Retrieve all the messages added after our last user message
    messages = client.beta.threads.messages.list(
        thread_id=assistant_thread.id, order="asc", after=message.id
    )

    
    # Append the assistant's responses to the session state
    for msg in messages.data:
        if msg.role == "assistant":
            st.session_state.conversation_history.append(("assistant", msg.content[0].text.value))  # Append assistant response


if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

def submit():
    user_input = st.session_state.query
    if user_input:  # Check if the user has entered any text
        # Append user input to conversation history before processing
        st.session_state.conversation_history.append(("user", user_input))
        # Get assistant's response
        get_assistant_response(user_input)
        # Clear the input field
        st.session_state.query = ''
# Function to render message parts
def render_message(message):
    # Split the message into parts using a regex to detect LaTeX expressions
    parts = re.split(r'(\[.*?\])', message)
    for part in parts:
        if part.startswith('[') and part.endswith(']'):
            latex_code = part[1:-1].strip()  # Remove the square brackets and strip whitespace
            try:
                st.latex(latex_code)
            except Exception as e:
                st.error(f"Error rendering LaTeX: {e}\nLaTeX code: {latex_code}")
        else:
            st.markdown(part)

for role, message in st.session_state.conversation_history:
    if role == 'user':
        st.markdown(f"<b style='color: yellow;'>{message}</b>", unsafe_allow_html=True)
    else:
        render_message(message)
st.text_input("What do you say?", key='query', on_change=submit)
