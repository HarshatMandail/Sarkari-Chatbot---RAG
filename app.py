import streamlit as st
from rag_backend import rag_pipeline

st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.title("🗂️ SARKARI CHATBOT")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field
user_input = st.text_input("Ask a question:")

# When user submits the query
if st.button("Ask"):
    if user_input.strip():
        # Call your RAG pipeline with the document name if needed
        answer, sources = rag_pipeline(user_input)

        # Append to session state
        st.session_state.chat_history.append({
            "user": user_input,
            "bot": answer,
            "sources": sources
        })
    else:
        st.warning("Please enter a question before submitting.")

# Display chat history
for chat in st.session_state.chat_history:
    st.markdown(f"**Query:** {chat['user']}")
    st.markdown(f"**ChatBot:** {chat['bot']}")
    if chat["sources"]:
        st.markdown(f"**Source:** {', '.join(chat['sources'])}")
    st.write("---")
