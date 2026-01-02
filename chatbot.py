import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

with st.sidebar:
    st.title("🔧 Debug")
    st.success("✅ Key loaded!")
    st.caption(api_key[:15] + "...")

if not api_key:
    st.error("Add GOOGLE_API_KEY to .env")
    st.stop()

genai.configure(api_key=api_key)

# ✅ Use current stable model (2026)
model = genai.GenerativeModel('gemini-2.5-flash')  # Fast, accessible, 1M context

# Vedaniti system prompt
model.system_instruction = """You are Vedaniti Technologies AI assistant (vedaniti.com).
Help with web/mobile apps, AI solutions, company services. Professional & concise."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Vedaniti AI ready! Ask about our services."}]

st.title("🤖 Vedaniti Chatbot")
st.caption("Google Gemini 2.5 | For vedaniti.com")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Cleared! How can I help?"}]
        st.rerun()
