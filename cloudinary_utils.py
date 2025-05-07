import cloudinary
import cloudinary.uploader
import streamlit as st

# Configure from Streamlit secrets
cloudinary.config(
    cloud_name=st.secrets["cloud_name"],
    api_key=st.secrets["api_key"],
    api_secret=st.secrets["api_secret"]
)

def upload_screenshot_to_cloudinary(image_path):
    try:
        response = cloudinary.uploader.upload(image_path)
        return response.get("secure_url")
    except Exception as e:
        print(f"Upload failed: {e}")
        return None
