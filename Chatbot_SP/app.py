import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(page_title="SP Chatbot", page_icon="🤖")
st.title("Oasis Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=10000,
            stream=True
        )

        full_response = ""
        message_placeholder = st.empty()

        for chunk in response:
            content = chunk.choices[0].delta.content
            if content is not None:
                full_response += content
                message_placeholder.markdown(full_response + "▌")

        # Final clean response
        message_placeholder.markdown(full_response)

        # Save to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
