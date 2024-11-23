import cv2
import numpy as np
import subprocess
import yt_dlp
import time
import os
import base64
import json
from datetime import datetime

# Define constants
youtube_url = 'https://www.youtube.com/live/gFRtAAmiFbE?si=L13Lyq4dNpBqVka3'
quality_threshold = 300
capture_duration = 45  # seconds
max_attempts = 5
retry_interval = 5  # seconds between retries

start_time = time.time()
best_frame = None
best_quality = 0

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

# Main capturing logic with retries
def capture_best_frame():
    global best_frame, best_quality
    attempts = 0
    stream_url = get_stream_url(youtube_url)
    
    while attempts < max_attempts and (time.time() - start_time) < capture_duration:
        if not stream_url:
            print("Failed to retrieve a valid stream URL. Exiting.")
            return False
        
        print(f"Attempt {attempts + 1}/{max_attempts} to capture frame...")

        # Define FFmpeg command to capture a single frame
        ffmpeg_command = [
            "ffmpeg",
            "-i", stream_url,
            "-frames:v", "1",  # Capture only 1 frame
            "-q:v", "2",       # High-quality image
            "-y",              # Overwrite output file
            "temp_frame.jpg"
        ]

        # Run FFmpeg command to capture a frame
        result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpeg_output = result.stderr.decode()
        print("FFmpeg log:", ffmpeg_output)

        # Attempt to load the saved frame with OpenCV
        frame = cv2.imread("temp_frame.jpg")
        if frame is None:
            print("Error reading frame from temp file. Retrying...")
            attempts += 1
            time.sleep(retry_interval)
            continue

        # Calculate quality and decide if it's the best frame so far
        quality = calculate_quality(frame)
        print(f"Captured frame quality: {quality}")

        if quality > best_quality:
            best_frame = frame.copy()
            best_quality = quality

        if quality > quality_threshold:
            print("Captured frame meets quality threshold. Stopping capture.")
            os.remove("temp_frame.jpg")  # Clean up
            return True  # Success

        os.remove("temp_frame.jpg")  # Clean up after each attempt
        attempts += 1

    print("Failed to capture a high-quality frame after multiple attempts.")
    return False

# Enhanced overlay function with outline for readability
def overlay_text(image, text, position):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    outline_thickness = 3  # Outline thickness
    color = (255, 255, 255)  # White text
    outline_color = (0, 0, 0)  # Black outline
    # Draw outline
    cv2.putText(image, text, position, font, font_scale, outline_color, outline_thickness, cv2.LINE_AA)
    # Draw text
    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

# Function to convert image to base64
def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode("utf-8")

# Execute capture and detection, and return results in JSON format
def main():
    static_config = {
        "user_id": "user_1",
        "DATE-TIME": datetime.now().isoformat(),  # Dynamically generate current date and time
        "config": {
            "Monitoring_status": True,
            "streaming_URL": "https://example.com/stream",
            "email": "user@example.com"
        }
    }
    
    if capture_best_frame():
        detected_frame, people_count = detect_people(best_frame)
        overlay_text(detected_frame, f"People Count: {people_count}", (10, 30))
        overlay_text(detected_frame, f"Source: {youtube_url}", (10, 60))

        # Convert images to base64
        best_frame_base64 = image_to_base64(best_frame)
        detected_frame_base64 = image_to_base64(detected_frame)

        # Return result as JSON
        result = {
            **static_config,
            "result": {
                "people_count": people_count
            },
            "processed_detection_image": detected_frame_base64
        }
        return json.dumps(result)
    else:
        return json.dumps({
            **static_config,
            "error": "Capture and detection process failed."
        })

if __name__ == "__main__":
    result_json = main()
    print(result_json)
