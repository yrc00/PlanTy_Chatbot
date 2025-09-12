import os
import streamlit as st

from src.chatbot import sidebar, chatbot

# ======================== 챗봇 설정 ========================

st.set_page_config(page_title="Planty Agent", page_icon="🌱")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_choice" not in st.session_state:
    st.session_state.api_choice = None

# ======================== 챗봇 실행 ========================

if __name__ == "__main__":
    st.title("🌱 Planty Agent")
    sidebar()
    chatbot()

