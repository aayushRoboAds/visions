# create a post request to localhost:5000/detect-face using streamlit
import streamlit as st
import requests
import os
import io
import hashlib

#set page title and icon
st.set_page_config(page_title="Face Detection", page_icon=":camera:", layout="wide")
# Function to upload image and get face detection results
def upload_image(image):
    url = "http://localhost:5000/detect-face"
    files = {"image": image}
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error in face detection")
        return None
# Streamlit app layout
st.title("Face Detection App")
st.write("Upload an image to detect faces.")
# File uploader for image input
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
a,b = st.columns([1, 1])
if uploaded_file is not None:
    # Display the uploaded image
    a.image(uploaded_file, caption="Uploaded Image", use_container_width=False)
    
    # Convert the uploaded file to bytes
    image_bytes = io.BytesIO(uploaded_file.read())
    
    # Call the upload_image function to get face detection results
    results = upload_image(image_bytes)
    
    if results:
        b.write(results["verified"])
        b.code(results["matched_face"])
    else:
        b.write("No faces detected or an error occurred.")

