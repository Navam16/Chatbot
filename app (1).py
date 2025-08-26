import streamlit as st
import google.generativeai as genai

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Gemini 1.5 Flash Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Gemini 1.5 Flash Chatbot")
st.write("Ask me anything, powered by Google's Gemini 1.5 Flash model.")

# --- Load API Key from Streamlit Secrets ---
# Create secrets.toml in .streamlit folder with: GEMINI_API_KEY = "your_api_key_here"
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🚨 API Key not found! Please add it in `.streamlit/secrets.toml`.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- Initialize Model ---
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input ---
user_input = st.chat_input("Type your question here...")
if user_input:
    # Save User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.generate_content(user_input)
            bot_reply = response.text
            st.markdown(bot_reply)

    # Save Assistant Reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
