import streamlit as st
import base64
from utils import get_response

# Page configuration
st.set_page_config(
    page_title="Simple AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Function to load video
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_video(video_file):
    bin_str = get_base64_of_bin_file(video_file)
    page_bg_video = f"""
    <style>
    .stApp {{
        background: transparent;
    }}
    video#bg-video {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        object-fit: cover;
    }}
    </style>
    <video autoplay muted loop id="bg-video">
        <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
    </video>
    """
    st.markdown(page_bg_video, unsafe_allow_html=True)

# Load background video if exists
try:
    set_background_video("background.mp4")
except Exception:
    # Fail silently if video missing
    pass

# Load custom CSS
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    load_css()
except FileNotFoundError:
    pass

# Sidebar for Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Get your key from https://aistudio.google.com/"
    )

    if not api_key:
        st.warning("⚠️ Enter API Key for AI features.")
    else:
        st.success("✅ API Key loaded.")

    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "This chatbot uses **Google Gemini** to provide real-life "
        "explanations and source recommendations."
    )

# Header
st.title("🤖 Intelligent AI Chatbot")
st.markdown("Welcome! Ask me anything, and I'll explain it with real-life examples.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        avatar = "me_icon.png"
    else:
        avatar = "ai_icon.png"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user", avatar="me_icon.png"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="ai_icon.png"):
        with st.spinner("Thinking..."):
            response = get_response(prompt, api_key=api_key)
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
