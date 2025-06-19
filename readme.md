# Vision Setup for Avatars

## Installation

1. Clone the repository and navigate to the project folder:
    ```sh
    git clone <repo-url> && cd face-recognition
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

---

## Step 1: Start Face Recognition Server & Test with Streamlit UI

1. Start the Flask server for facial recognition:
    ```sh
    python app.py
    ```
2. Add images of known faces to the folder.
3. Test face recognition manually using Streamlit:
    ```sh
    streamlit run frontend.py
    ```

---

## Step 2: Start Mic Control & Polling File Control

1. Start mic and file control:
    ```sh
    python mic.py
    ```
2. The camera will open, detect humans, and send images to the Flask server.
3. Press `Q` to stop the camera.

---

## Step 3: Local Avatar Code Snippet

1. Paste the following code in your `simliOpenAI.tsx` file:

    ````typescript
    useEffect(() => {
        const faceInterval = setInterval(async () => {
            try {
                // ✅ Fetch your .txt file (it must be served from your public folder or a URL)
                const response = await fetch("/face_status.txt");
                const text = await response.text();
                const faceStatus = text.trim().toLowerCase() === "true";

                // ✅ Your original condition using simliClient
                if (!simliClient.isAvatarSpeaking) {
                    if (faceStatus) {
                        console.log("Face detected from file:", faceStatus);
                        openAIClientRef.current?.sendUserMessageContent([{
                            type: "input_text",
                            text: "New face detected. Wish and welcome the new user."
                        }]);
                    }
                }
            } catch (error) {
                console.error("Error fetching face status:", error);
            }
        }, 1000); // every 1 second

        // ✅ Clean up interval when component unmounts
        return () => clearInterval(faceInterval);
    }, []);
    ````

2. Start the avatar interaction:
    ```sh
    npm run dev
    ```

---

## Summary

This setup provides vision capabilities to your avatar, enabling it to detect faces and respond