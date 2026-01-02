import os
import streamlit as st
import google.generativeai as genai  # CORRECT IMPORT
import requests
from bs4 import BeautifulSoup

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

# 🌐 Vedaniti website context (RAG)
VEDANITI_CONTEXT = """
Vedaniti Technologies: Empowering businesses with cutting-edge technology.
Services: Custom software development (scalable, secure apps), Websites (stunning UI/UX), 
Mobile apps (iOS/Android), Edtech platforms, AI solutions.
Mission: Transform ideas into digital solutions. Projects delivered, happy clients.
Website: vedaniti.com
"""

def get_website_context(query):
    """Fetch vedaniti.com if query mentions Vedaniti/services"""
    if any(word in query.lower() for word in ['vedaniti', 'services', 'service', 'website', 'app', 'software']):
        try:
            response = requests.get("https://vedaniti.com", timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract key sections (customize selectors)
            services = soup.find_all(['p', 'h2', 'h3'], string=lambda t: t and 'services' in t.lower())
            context = ' '.join([s.get_text() for s in services[:3]])[:2000]
            return f"Vedaniti website: {context}"
        except:
            return VEDANITI_CONTEXT
    return VEDANITI_CONTEXT

# Vedaniti-aware system prompt
model.system_instruction = f"""You are 'Ask Me' - Vedaniti's AI assistant.
Vedaniti context: {VEDANITI_CONTEXT}

Answer ALL queries using Vedaniti knowledge when relevant. Be helpful, professional.
For Vedaniti questions: Use website context + services info."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm Ask Me 🤖 Vedaniti's AI assistant. Ask about our services, apps, or anything!"}]

st.title("🤖 Ask Me AI Assistant")
st.caption("Powered by Google Gemini 2.5 | Vedaniti-aware")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Vedaniti services?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # RAG: Add website context
                context = get_website_context(prompt)
                full_prompt = f"Vedaniti context: {context}\n\nUser: {prompt}"
                
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
        st.session_state.messages = [{"role": "assistant", "content": "Cleared! Ask about Vedaniti? 😊"}]
        st.rerun()
    
    st.metric("Messages", len(st.session_state.messages))
    st.caption("✅ Vedaniti RAG enabled")
