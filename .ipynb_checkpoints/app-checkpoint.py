# app.py

import streamlit as st
from rag_backend import rag_pipeline

st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.title("SARKARI CHATBOT")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.text_input("Ask a question:")

if st.button("Ask"):

    if user_input:
        answer, sources = rag_pipeline(user_input)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", answer))
        st.session_state.chat_history.append(("Source", ", ".join(sources)))

# Display chat
for role, text in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 You:** {text}")
    elif role == "Bot":
        st.markdown(f"**🤖 Bot:** {text}")
    else:
        st.markdown(f"**📚 Source:** {text}")