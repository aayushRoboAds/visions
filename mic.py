import cv2
import subprocess
import time
#from camxmic.mute import mute
# from . import mute
import mute  # Assuming mute.py is in the same directory
import requests

def upload_image(image):
    url = "http://localhost:5000/detect-face"
    files = {"image": image}
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        # st.error("Error in face detection")
        return None
# Human detection setup
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

mic_on = False
last_seen_time = 0

# Change this to 5 or any duration you want to wait before turning off mic
HUMAN_TIMEOUT = 5
RUN_NUMBER = 0  # increase this after every run


# Start camera
cap = cv2.VideoCapture(0)
print("Press 'q' to quit.")

while True:
    RUN_NUMBER += 1
    ret, frame = cap.read()
    if not ret:
        break

    # Detect humans
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects, _ = hog.detectMultiScale(gray, winStride=(4, 4), padding=(8, 8), scale=1.05)

    now = time.time()

    if len(rects) > 0: #human detected
        last_seen_time = now
         # cAPTURE IMAGE OF HUMAN AND CREATE A FILE
        image_path = r"D:\ROBOADS\property_local_LED\public\human_detected.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image saved at {image_path} 📸")

        # Upload image to server
        with open(image_path, "rb") as image_file:
            response = upload_image(image_file)
            print("Response from server:", response)
        if response and "verified" in response:
            if response["verified"] == True:
                print("Old Face! Response:", response)
            else:
                print("New Face! Response:", response)
                with open(r"D:\ROBOADS\property_local_LED\public\face_status.txt", "w") as f:
                    f.write("true")
                    print("Written true to face_status.txt ✅")
        else:
            print("Error: Invalid response from server or 'verified' key missing.")
            
                
        if not mic_on: # mic is off and human detected
            
            mute.mute_microphone(False)  # Ensure mic is on
            mic_on = True

           
        else:
            
            print(f"Human detected, mic already on 🟢: Iteration  {RUN_NUMBER}")
            if RUN_NUMBER % 10 == 0:  # Every 8 runs, write to file
                with open(r"D:\ROBOADS\property_local_LED\public\face_status.txt", "w") as f:
                    f.write("false")
                print("Written false to face_status.txt ❌")
                
                
            
    elif mic_on and (now - last_seen_time > HUMAN_TIMEOUT):
        mute.mute_microphone(True)
        mic_on = False
        # write false on a file to be read by another process
        with open(r"D:\ROBOADS\property_local_LED\public\face_status.txt", "w") as f:
            f.write("false")
            print("Written false to face_status.txt ❌")

    # print(f"Mic {'🟢 MIC ON' if mic_on else '🔴MIC OFF'} - Humans detected: {len(rects)} - {RUN_NUMBER}")
    # Display
    if mic_on:
        cv2.putText(frame, "Mic ON (Human detected)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Mic OFF", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Mic Control - Human Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
