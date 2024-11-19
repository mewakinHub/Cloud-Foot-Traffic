import requests
import time
import cv2
import os
import json
from datetime import datetime

# Shotstack API configuration
SHOTSTACK_API_KEY = "pG9EMlF4g5awLHozfjyWeqzwLa6QPfG05IAHmS3u"  # Replace with your Shotstack API key
SHOTSTACK_API_URL = "https://api.shotstack.io/stage/render"

# Constants for processing
YOUTUBE_LIVE_URL = "https://www.youtube.com/live/gFRtAAmiFbE?si=L13Lyq4dNpBqVka3"
OUTPUT_IMAGE_PATH = "./local_vol/output_images"
QUALITY_THRESHOLD = 300

def submit_shotstack_job(youtube_url):
    """Submits a render job to Shotstack for frame extraction."""
    payload = {
        "timeline": {
            "tracks": [
                {
                    "clips": [
                        {
                            "asset": {"type": "video", "src": youtube_url},
                            "start": 0,
                            "length": 5,  # Process up to 5 seconds of video
                            "fit": "cover"
                        }
                    ]
                }
            ]
        },
        "output": {"format": "jpg", "fps": 30}  # Use 30 fps as it's supported
    }
    headers = {"x-api-key": SHOTSTACK_API_KEY, "Content-Type": "application/json"}
    response = requests.post(SHOTSTACK_API_URL, json=payload, headers=headers)
    if response.status_code == 201:
        print("Shotstack render job submitted successfully.")
        return response.json().get("id")
    else:
        print("Failed to submit render job:", response.text)
        return None

def poll_job_status(job_id):
    """Polls the Shotstack job status until it's completed."""
    headers = {"x-api-key": SHOTSTACK_API_KEY}
    status_url = f"{SHOTSTACK_API_URL}/{job_id}"

    while True:
        response = requests.get(status_url, headers=headers)
        data = response.json()

        status = data.get("status")
        print(f"Job Status: {status}")

        if status == "done":
            print("Job completed successfully.")
            return data.get("url")
        elif status == "failed":
            print("Job failed:", response.text)
            return None

        time.sleep(5)  # Wait 5 seconds before polling again

def download_frame(url, output_path):
    """Downloads the rendered frame from Shotstack."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Frame saved to {output_path}.")
    else:
        print("Failed to download frame:", response.text)

def detect_people(frame_path):
    """Detects people in the given frame using OpenCV."""
    frame = cv2.imread(frame_path)
    if frame is None:
        print("Error loading frame for detection.")
        return None, 0

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    boxes, _ = hog.detectMultiScale(frame, winStride=(8, 8))

    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame, len(boxes)

def main():
    # Create output directory if not exists
    os.makedirs(OUTPUT_IMAGE_PATH, exist_ok=True)

    # Submit Shotstack render job
    job_id = submit_shotstack_job(YOUTUBE_LIVE_URL)
    if not job_id:
        print("Failed to start render job.")
        return

    # Poll for job completion
    render_url = poll_job_status(job_id)
    if not render_url:
        print("Failed to complete render job.")
        return

    # Download the rendered frame
    output_frame_path = os.path.join(OUTPUT_IMAGE_PATH, "output_frame.jpg")
    download_frame(render_url, output_frame_path)

    # Detect people in the frame
    processed_frame, people_count = detect_people(output_frame_path)
    if processed_frame is not None:
        output_detected_path = os.path.join(OUTPUT_IMAGE_PATH, "detected_people.jpg")
        cv2.imwrite(output_detected_path, processed_frame)
        print(f"Processed frame saved to {output_detected_path}.")
        print(f"People detected: {people_count}")

        # Output result as JSON
        result = {
            "timestamp": datetime.now().isoformat(),
            "youtube_url": YOUTUBE_LIVE_URL,
            "people_count": people_count,
            "processed_frame_path": output_detected_path
        }
        print(json.dumps(result, indent=4))
    else:
        print("No people detected.")

if __name__ == "__main__":
    main()
