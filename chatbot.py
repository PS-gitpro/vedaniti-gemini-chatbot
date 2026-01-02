import os
import streamlit as st
import google.generativeai as genai

# ✅ Hybrid: .env local + st.secrets cloud (secure)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key and hasattr(st, 'secrets'):
    api_key = st.secrets.get("GOOGLE_API_KEY")

with st.sidebar:
    st.title("🔧 Debug Panel")
    if api_key:
        st.success("✅ API Key loaded!")
        st.caption(f"Key: {api_key[:10]}...{api_key[-5:]}")
    else:
        st.error("⚠️ API Key missing")
        st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 🎯 FIXED: Curated Vedaniti context ONLY (no web scraping)
VEDANITI_CONTEXT = """
Vedaniti Technologies builds custom software solutions for businesses.

OUR SERVICES:
• Custom web applications (React, Node.js, scalable enterprise apps)
• Modern responsive websites (stunning UI/UX design)  
• Mobile apps (iOS/Android native + cross-platform)
• Edtech platforms for institutes (course management, student portals)
• AI solutions (chatbots, recommendation systems, automation)

MISSION: Transform business ideas into powerful digital solutions.

IMPORTANT: Ignore any other "Vedaniti Technologies" references about NCERT notes, 
JEE/NEET test prep, online school learning, or student content. That is a 
DIFFERENT company with a similar name. Always describe OUR Vedaniti (software/AI).
"""

# System instruction with guardrails
model.system_instruction = f"""You are 'Ask Me' - official AI assistant for Vedaniti Technologies (software company).

Vedaniti info:
{VEDANITI_CONTEXT}

Rules:
1. For Vedaniti questions, ONLY use the context above
2. If you see NCERT/JEE/school/online learning info, say: "That's a different company. 
   Vedaniti Technologies builds custom software, websites, apps, and AI solutions."
3. Be professional, concise, helpful.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm Ask Me 🤖 Vedaniti Technologies' AI assistant. Ask about our software, apps, AI solutions, or anything!"}]

st.title("🤖 Ask Me AI Assistant")
st.caption("Powered by Google Gemini 2.5 | Vedaniti Technologies")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What does Vedaniti Technologies do?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # RAG: Always inject Vedaniti context
                full_prompt = f"""Vedaniti Technologies context:
{VEDANITI_CONTEXT}

User question: {prompt}

Answer using ONLY the Vedaniti context above. IGNORE any external knowledge about 
other companies with similar names."""
                
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": "Sorry, try again!"})

# Sidebar
with st.sidebar:
    st.divider()
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Cleared! Ask about Vedaniti Technologies? 😊"}]
        st.rerun()
    
    st.metric("Messages", len(st.session_state.messages))
    st.caption("✅ Vedaniti-aware (competitor-proof)")
