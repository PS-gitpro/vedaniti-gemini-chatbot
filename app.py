import os
import time
import streamlit as st
from groq import Groq

# --- 1. SECURE CONFIGURATION ---
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ API Key missing! Add GROQ_API_KEY to your Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# ✅ FIXED: Active model (Jan 2026)
MODEL_ID = "llama-3.3-70b-versatile"

# --- 2. EXPANDED VEDANITI KNOWLEDGE BASE (from vedaniti.com) ---
VEDANITI_CONTEXT = """
Vedaniti Technologies (https://vedaniti.com/) - Empowering businesses with cutting-edge technology solutions.

SERVICES:
- Custom Software Development: Scalable, secure, high-performance apps tailored to business needs.
- Website Design: Visually stunning, user-friendly websites with seamless browsing experience.
- Mobile Apps: Intuitive, feature-rich iOS/Android apps that meet business goals.
- UI/UX Design
- Edtech Solutions
- AI/ML Integration & Chatbots

STATS (from homepage):
- Projects Delivered: 50+
- Happy Clients: 30+
- Team Members: 15+

MISSION: Transform business ideas into powerful digital solutions. 'Innovate. Build. Grow.'

COMMON QUERIES & RESPONSES:
- Pricing? Flexible packages starting from project scope discussion. Free consultation.
- Timeline? 2-12 weeks based on complexity. Agile development.
- Portfolio? View live projects at vedaniti.com/portfolio (coming soon).
- Contact? Email: hello@vedaniti.com | LinkedIn/Twitter links on site.
- Tech Stack? React/Node.js, Flutter, Python AI/ML, GCP/AWS deployment.

KEY POINT: SOFTWARE DEVELOPMENT AGENCY, NOT test prep/schooling. Redirect education queries to edtech custom solutions.

TONE: Professional, helpful, solution-focused.
"""

SYSTEM_PROMPT = f"""You are 'Ask Me' - the AI Assistant for Vedaniti Technologies (vedaniti.com).

KNOWLEDGE BASE:
{VEDANITI_CONTEXT}

RULES:
1. Answer ONLY using this knowledge base + vedaniti.com content.
2. For new topics, say: "Great question! Let's discuss in a free consultation at vedaniti.com/contact."
3. Concise: 2-4 sentences max.
4. Handle pricing/timeline/portfolio with specifics above.
5. Professional, action-oriented. End with CTA: "Ready to start? Visit vedaniti.com"

RESPONSE STYLE: Friendly, confident.
"""

# --- 3. STREAMLIT UI SETUP (unchanged) ---
st.set_page_config(
    page_title="Vedaniti AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Ask Me AI Assistant")
st.caption("Vedaniti Technologies | Powered by Groq (LLaMA 3.3 70B) | vedaniti.com")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I'm Ask Me from Vedaniti Technologies (vedaniti.com). Ask about our custom software, websites, mobile apps, or stats like 50+ projects delivered!"
        }
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. CHAT INPUT & PROCESSING (unchanged) ---
if prompt := st.chat_input("Ask about Vedaniti services, pricing, timeline..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("⚡ Thinking..."):
            max_retries = 3
            initial_delay = 5
            
            for attempt in range(max_retries):
                try:
                    response = client.chat.completions.create(
                        model=MODEL_ID,
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,
                        max_tokens=256,
                        top_p=0.95,
                    )
                    
                    response_text = response.choices[0].message.content
                    st.markdown(response_text)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text
                    })
                    break
                
                except Exception as e:
                    error_msg = str(e)
                    
                    if "429" in error_msg or "rate_limit" in error_msg.lower():
                        if attempt < max_retries - 1:
                            wait_time = initial_delay * (attempt + 1)
                            st.warning(
                                f"⏳ Rate limit. Retrying in {wait_time}s... ({attempt + 1}/{max_retries})"
                            )
                            time.sleep(wait_time)
                        else:
                            st.error("⚠️ Service temporarily busy. Please wait a moment.")
                    else:
                        st.error(f"❌ Error: {error_msg[:100]}")
                        break

# --- 5. ENHANCED SIDEBAR ---
with st.sidebar:
    st.markdown("### 🎛️ Controls")
    
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Chat cleared!"}]
        st.rerun()
    
    st.divider()
    
    st.markdown("### 📊 Vedaniti Stats")
    st.info("**50+ Projects | 30+ Clients | 15 Team** [page:1]")
    
    st.markdown("### ⚡ About Groq")
    st.info(
        "**Groq + LLaMA 3.3 70B**\n"
        "• 280 tokens/sec\n"
        "• Free: 30 req/min"
    )
    
    st.markdown("[vedaniti.com](https://vedaniti.com/)")
