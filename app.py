from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai 
from PIL import Image

genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):

    model = genai.GenerativeModel("gemini-1.5-flash-001")
    response = model.generate_content([input_prompt, image[0]])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:

        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data

            }
        ]
        return image_parts
    else: 
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title= "Detect AI generated or Real image")

st.header("LLM application to check AI generated image or real image")

# input = st.text_input("input: ", key = "input")

uploaded_file = st.file_uploader("choose an image...", type= ["jpg","jpeg","png"])
image = ""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded image", use_column_width=True)

submit = st.button("Check AI or Real...")

input_prompt = """Can you analyze this image and determine whether it is AI-generated or not?

            Also mention in the format:
            
            confidence that AI: 50%
            confidence that Real: 50%

            lastly leave a gentle message that: you are still learning so you may wrong sometimes
"""



if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.header("The response is...")
    st.write(response)