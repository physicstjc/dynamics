import os
import streamlit as st
from openai import OpenAI
# from openai import OpenAI
client = OpenAI(
	api_key=os.environ['OPENAI_API_KEY'], 
)

# Initialize OpenAI
# openai.api_key = os.getenv('OPENAI_API_KEY')


st.title("Physics Tutor")
st.text("Ask me a Physics question!")
#Change here onwards

	
# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Speak like a friend who is very good in physics. Explain in a succinct and clearly manner, with no more than 300 words per key idea, assuming the students know very little prior knowledge. Display answers with mathematical content using LaTeX markup, within a pair of $ symbols, for clear and precise presentation. Ensure all equations, formulas, and mathematical expressions are correctly formatted in LaTeX. If relevant, make reference to actual webpages in Wikipedia by replacing the {search+terms} placeholder with the search terms in 'https://en.wikipedia.org/w/index.php?search={search+terms}', showing it as a link."},]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
	    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
	
