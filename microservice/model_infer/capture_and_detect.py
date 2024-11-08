import cv2
import numpy as np
import subprocess
import yt_dlp
import time
import os

# Define constants
youtube_url = 'https://www.youtube.com/live/DjdUEyjx8GM?si=tZG-w_TURjZSQtNn'

output_image_path = "/app/output_images/output_frame.jpg"
detected_image_path = "/app/output_images/detected_people.jpg"
temp_image_path = "/app/output_images/temp_frame.jpg"  # Temporary file path

quality_threshold = 300
capture_duration = 45  # seconds
max_attempts = 5
retry_interval = 5  # seconds between retries

# Initialize variables
start_time = time.time()
best_frame = None
best_quality = 0

# Function to retrieve a direct video URL using yt-dlp
def get_stream_url(youtube_url):
    try:
        ydl_opts = {
            'format': 'best[height<=1080]',  # Restrict to 1080p or lower for stability
            'quiet': True
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

        # Define FFmpeg command to save a frame to a file
        ffmpeg_command = [
            "ffmpeg",
            "-i", stream_url,
            "-frames:v", "1",  # Capture only 1 frame
            "-q:v", "2",       # High-quality image
            "-y",              # Overwrite output file
            temp_image_path
        ]

        # Run FFmpeg command to capture a frame
        result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpeg_output = result.stderr.decode()
        print("FFmpeg log:", ffmpeg_output)

        # Verify if the file was created and has content
        if not os.path.exists(temp_image_path) or os.path.getsize(temp_image_path) == 0:
            print("Failed to capture frame: temp file is empty or missing.")
            attempts += 1
            if attempts % 2 == 0:  # Every 2nd failed attempt, refresh the stream URL
                stream_url = get_stream_url(youtube_url)
            time.sleep(retry_interval)
            continue

        # Attempt to load the saved frame with OpenCV
        frame = cv2.imread(temp_image_path)
        if frame is None:
            print("Error reading frame from temp file. Retrying...")
            attempts += 1
            os.remove(temp_image_path)  # Clean up before retrying
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
            os.remove(temp_image_path)  # Clean up
            return True  # Success

        os.remove(temp_image_path)  # Clean up after each attempt
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

# Execute capture and detection
if capture_best_frame():
    detected_frame, people_count = detect_people(best_frame)
    overlay_text(detected_frame, f"People Count: {people_count}", (10, 30))
    overlay_text(detected_frame, f"Source: {youtube_url}", (10, 60))

    cv2.imwrite(output_image_path, best_frame)
    cv2.imwrite(detected_image_path, detected_frame)
    print(f"Frame saved as {output_image_path} and {detected_image_path}")
else:
    print("Capture and detection process failed.")
