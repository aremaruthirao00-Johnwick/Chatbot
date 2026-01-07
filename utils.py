import random
import google.generativeai as genai

def get_response(user_input, api_key=None):
    """
    Returns a response based on rule-based logic or LLM if available.
    """
    user_input = user_input.lower().strip()

    # 1. Try Gemini API first if key is provided
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # System prompt to encourage real-life answers and sources
            prompt = f"""
            You are a helpful and knowledgeable AI assistant.
            The user has asked: "{user_input}"
            
            Please provide a comprehensive answer that:
            1. Explains the concept in simple, real-life terms.
            2. Provides examples where applicable.
            3. Recommends credible sources (books, websites, papers) for further reading if the topic allows.
            
            Keep the tone friendly and professional.
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error using Gemini API: {str(e)}\n\n(Falling back to simple mode...)"

    # 2. Rule-based Fallback
    # Greetings
    if user_input in ["hi", "hello", "hey", "greetings"]:
        return random.choice([
            "Hello! How can I help you today?",
            "Hi there! What's on your mind?",
            "Greetings! ready to chat."
        ])
    
    # Identification
    elif "who are you" in user_input or "what are you" in user_input:
        return "I am a simple AI chatbot built with Streamlit and Python. Add a Gemini API Key to unlock my full potential!"

    # Help
    elif "help" in user_input or "assist" in user_input:
        return "I can answer simple questions. To get detailed real-life explanations, please enter a Google Gemini API Key in the sidebar."
    
    # Default fallback
    else:
        return random.choice([
            "I'm currently in simple mode. To get detailed answers and real-life examples, please enter an API Key!",
            "I don't have access to my brain right now. Please provide an API Key.",
            "That sounds complex! Enable my AI powers with an API Key to answer that."
        ])
