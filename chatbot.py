import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# ✅ Try Streamlit secrets as fallback for cloud deployment
if not api_key and hasattr(st, 'secrets'):
    api_key = st.secrets.get("GOOGLE_API_KEY")

with st.sidebar:
    st.title("🔧 Debug Panel")
    if api_key:
        st.success("✅ API Key loaded successfully!")
        st.caption(f"Key: {api_key[:10]}...{api_key[-5:]}" if len(api_key) > 15 else "Key loaded")
    else:
        st.error("⚠️ API Key not found")
        st.info("Add GOOGLE_API_KEY to .env file or Streamlit secrets")

if not api_key:
    st.error("🚨 API Key Required: Add GOOGLE_API_KEY to .env or Streamlit secrets")
    st.info("Get your key from: https://makersuite.google.com/app/apikey")
    st.stop()

genai.configure(api_key=api_key)

# ✅ Use current stable model (2026)
model = genai.GenerativeModel('gemini-2.5-flash')  # Fast, accessible, 1M context

# Updated system prompt for "Ask me" branding
model.system_instruction = """You are 'Ask Me' - a helpful AI assistant designed to answer questions clearly and concisely. 
Provide accurate, informative responses. Be friendly but professional. If you don't know something, admit it honestly."""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm Ask Me 🤖 How can I help you today?"}]

# Main UI
st.title("🤖 Ask Me AI Assistant")
st.caption("Powered by Google Gemini 2.5 | Ask me anything!")

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar controls
with st.sidebar:
    st.divider()
    st.subheader("Chat Controls")
    
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Chat cleared! I'm ready for your questions. 😊"}]
        st.rerun()
    
    st.divider()
    st.subheader("ℹ️ About")
    st.markdown("""
    **Ask Me AI Assistant**
    
    Powered by Google's Gemini 2.5 Flash model.
    
    Features:
    - Real-time conversations
    - Fast responses
    - Context-aware replies
    
    Built with Streamlit + Gemini API
    """)
    
    # Show message count
    st.divider()
    st.metric("Messages", len(st.session_state.messages))
