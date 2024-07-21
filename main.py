import os
import streamlit as st
from openai import OpenAI

# Initialize OpenAI
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

st.title("IP3 Physics Dynamics Bot")
st.text("I'm here to help!")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Speak like a friend who is very good in physics. Explain in a succinct and clearly manner, with no more than 200 words per key idea, assuming the students know very little prior knowledge. Display answers with mathematical content using LaTeX markup, within a pair of $ symbols, for clear and precise presentation. Ensure all equations, formulas, and mathematical expressions are correctly formatted in LaTeX. Ensure that the conversation is focused on the Physics topics of Dynamics at the middle school level, with the learning objectives being the following: factors that affect forces such as normal contact force, weight, friction, air resistance, elastic spring force; Newton's three laws of motion; solving word problems using free body diagrams representing the forces acting on the body for cases involving forces acting in at most two dimensions."}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What questions do you still have about Dynamics?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Generate response from OpenAI API
    with st.chat_message("assistant"):
        stream = client.chat_completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = ""
        for chunk in stream:
            response += chunk["choices"][0]["delta"]["content"]
            st.markdown(chunk["choices"][0]["delta"]["content"])
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Render LaTeX in response
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f"$$ {message['content']} $$")
