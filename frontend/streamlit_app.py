import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
from backend.build_index import build_index

st.set_page_config(page_title="Customer Support Chatbot", page_icon="🤖")
st.title("📞 Customer Support Chatbot")

if st.button("Build Index"):
    with st.spinner("Running... Please wait."):
        result = build_index()
    st.success(result)

query = st.text_input("Ask a question...")

if query:
    with st.spinner("Thinking..."):
        response = requests.post("http://localhost:8000/ask", json={"query": query})
        answer = response.json().get("answer", "Something went wrong.")
        st.markdown(f"**Answer :** {answer}")