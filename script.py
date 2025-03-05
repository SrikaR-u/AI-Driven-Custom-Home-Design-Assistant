# AI-Driven-Custom-Home-Design-Assistant

import streamlit as st
import google.generativeai as genai
import requests  # For API requests

# Configure API Key for Google Gemini
api_key = "YOUR_GOOGLE_GENAI_API_KEY"  # Replace with your actual Google API key
genai.configure(api_key=api_key)

# DeepAI API Key for Image Generation (Get it from https://deepai.org/)
DEEPAI_API_KEY = "YOUR_DEEPAI_API_KEY"

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# Function to generate home design ideas
def generate_design_idea(style, size, rooms):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )
    
    context = f"Create a custom home design plan with the following details:\nStyle: {style}\nSize: {size}\nRooms: {rooms}"
    
    chat_session = model.start_chat(
        history=[{"role": "user", "parts": [context]}]
    )

    response = chat_session.send_message(context)
    text = response.candidates[0].content if isinstance(response.candidates[0].content, str) else response.candidates[0].content.parts[0].text
    return text

# Function to generate images using DeepAI API
def generate_image_from_deepai(prompt):
    url = "https://api.deepai.org/api/text2img"
    headers = {"api-key": DEEPAI_API_KEY}
    data = {"text": prompt}

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("output_url")  # Returns the image URL
    return None

# Streamlit UI for taking user inputs
st.title("Custom Home Design Assistant")

# Textboxes for style, size, and number of rooms input
style = st.text_input("Enter the home design style (e.g., Modern, Rustic)")
size = st.text_input("Enter the size of the home (e.g., 2000 sq ft)")
rooms = st.text_input("Enter the number of rooms")

# Submit button
if st.button("Generate Design"):
    if style and size and rooms:
        design_idea = generate_design_idea(style, size, rooms)
        image_url = generate_image_from_deepai(f"{style} home design, {size}, {rooms} rooms")

        st.markdown("### Custom Home Design Idea")
        st.markdown(design_idea)

        if image_url:
            st.image(image_url, caption="AI-generated home design")
        else:
            st.warning("No image could be generated.")
    else:
        st.warning("Please fill in all the fields.")
