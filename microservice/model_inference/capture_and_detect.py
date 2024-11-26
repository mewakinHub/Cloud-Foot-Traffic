import os
import json
from datetime import datetime
import base64
import cv2
import subprocess
import time
import numpy as np
import yt_dlp

# Function to retrieve YouTube stream URL using yt-dlp
def get_stream_url(youtube_url):
    try:
        ydl_opts = {
            'format': '96',
            'quiet': True,
            'cookiefile': './cookie.txt',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            stream_url = info_dict['url']
            print("Successfully retrieved stream URL.")
            return stream_url
    except Exception as e:
        print("Error fetching stream URL with yt-dlp:", str(e))
        return None

# Function to calculate frame quality
def calculate_quality(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var

# Function to detect people in the frame
def detect_people(frame):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    boxes, _ = hog.detectMultiScale(frame, winStride=(8, 8))
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame, len(boxes)

# Function to capture the best frame
def capture_best_frame(youtube_url, capture_duration, quality_threshold, max_attempts=5, retry_interval=5):
    best_frame = None
    best_quality = 0
    start_time = time.time()
    attempts = 0
    stream_url = get_stream_url(youtube_url)

    while attempts < max_attempts and (time.time() - start_time) < capture_duration:
        if not stream_url:
            print("Failed to retrieve a valid stream URL. Exiting.")
            return False, None, None

        print(f"Attempt {attempts + 1}/{max_attempts} to capture frame...")

        ffmpeg_command = [
            "ffmpeg",
            "-i", stream_url,
            "-frames:v", "1",
            "-q:v", "2",
            "-y",
            "temp_frame.jpg"
        ]

        result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        frame = cv2.imread("temp_frame.jpg")
        if frame is None:
            print("Error reading frame from temp file. Retrying...")
            attempts += 1
            time.sleep(retry_interval)
            continue

        quality = calculate_quality(frame)
        print(f"Captured frame quality: {quality}")

        if quality > best_quality:
            best_frame = frame.copy()
            best_quality = quality

        if quality > quality_threshold:
            print("Captured frame meets quality threshold. Stopping capture.")
            os.remove("temp_frame.jpg")
            return True, best_frame, best_quality

        os.remove("temp_frame.jpg")
        attempts += 1

    print("Failed to capture a high-quality frame after multiple attempts.")
    return False, None, None

# Function to overlay text
def overlay_text(image, text, position):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    outline_thickness = 3
    color = (255, 255, 255)
    outline_color = (0, 0, 0)
    cv2.putText(image, text, position, font, font_scale, outline_color, outline_thickness, cv2.LINE_AA)
    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

# Function to convert image to Base64
def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode("utf-8")

# Main user processing function
def process_user(user):
    streaming_url = user["streaming_URL"]
    email = user["email"]
    username = user["username"]

    print(f"Processing user: {username} with stream URL: {streaming_url}")

    capture_duration = 45
    quality_threshold = 300
    date_time = datetime.now().isoformat()

    success, best_frame, best_quality = capture_best_frame(streaming_url, capture_duration, quality_threshold)

    if success:
        detected_frame, people_count = detect_people(best_frame)
        overlay_text(detected_frame, f"People Count: {people_count}", (10, 30))
        overlay_text(detected_frame, f"Source: {streaming_url}", (10, 60))

        detected_frame_base64 = image_to_base64(detected_frame)

        return {
            "username": username,
            "DATE_TIME": date_time,
            "result": {
                "people_count": people_count,
                "processed_detection_image": detected_frame_base64
            }
        }
    else:
        return {
            "username": username,
            "DATE_TIME": date_time,
            "error": "Failed to process due to poor stream quality"
        }

def main():
    """
    Main function to process the PAYLOAD environment variable and handle user-specific operations.
    """
    try:
        # Fetch the PAYLOAD environment variable
        payload = os.getenv("PAYLOAD")
        if not payload:
            raise ValueError("PAYLOAD environment variable is not set or empty.")
        print(f"[INFO] RAW PAYLOAD: {payload}")
        
        # Parse the PAYLOAD JSON
        try:
            payload_data = json.loads(payload)
        except json.JSONDecodeError as e:
            raise ValueError(f"[ERROR] Error parsing PAYLOAD JSON: {e}\nRAW PAYLOAD: {payload}")
        
        print(f"[INFO] Parsed PAYLOAD content: {json.dumps(payload_data, indent=4)}")

        # Validate required keys in payload
        required_keys = ["username", "streaming_URL", "email"]
        missing_keys = [key for key in required_keys if key not in payload_data]
        if missing_keys:
            raise ValueError(f"[ERROR] Missing required keys in PAYLOAD: {missing_keys}")

        # Extract user information
        username = payload_data["username"]
        streaming_url = payload_data["streaming_URL"]
        email = payload_data["email"]

        # Process user locally (for example, capture a frame)
        print(f"[INFO] Processing user: {username} with streaming URL: {streaming_url}")

        result = process_user(payload_data)

        # Return the result as a JSON string
        print(f"[INFO] Processing completed: {json.dumps(result, indent=4)}")
        return json.dumps(result)

    except ValueError as ve:
        print(f"[ERROR] ValueError: {ve}")
        return json.dumps({"status": "error", "message": str(ve), "timestamp": datetime.now().isoformat()})
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return json.dumps({"status": "error", "message": str(e), "timestamp": datetime.now().isoformat()})
# Entry point for execution
if __name__ == "__main__":
    """
    This block runs when the script is executed directly.
    It calls the `main` function and handles its output.
    """
    try:
        result = main()  # Call the main function
        print(f"[INFO] Main function execution result: {result}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred during execution: {e}")
