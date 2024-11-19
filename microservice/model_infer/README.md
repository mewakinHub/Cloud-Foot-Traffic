## License & Stream_URL:
video example of Japan foot traffic from:
https://www.youtube.com/live/gFRtAAmiFbE?si=L13Lyq4dNpBqVka3
https://www.youtube.com/live/DjdUEyjx8GM?si=2L7zK3QC2r_oaRnB

### 3. Build and Run the Docker Container

1. **Build the Docker Image**:
   Open a terminal in the directory containing your `Dockerfile` and `capture_and_detect.py`, then run:
   ```bash
   docker build -t youtube-human-detection .
   docker build --no-cache -t youtube-human-detection .
   ```

2. **Run the Docker Containerv for Local DEV (local_vol)**:
   To run the container and save the output images to your local machine, use volume mapping:
   ```bash
   # ubuntu (instance)
   cd ..
   docker run --rm -v $(pwd)/local_vol/output_images:/app youtube-human-detection
   
   # window (local)
   docker run --rm -v C:/Users/mew/Documents/github/Cloud-Foot-Traffic/microservice/local_vol/output_images:/app youtube-human-detection
   docker run --rm youtube-human-detection
   ```
   This command maps your current directory to the `/app` directory in the container, allowing the output images to be saved directly to your host machine.

   The --rm flag in Docker is used with the docker run command to automatically remove a container once it exits. This ensures that stopped containers don't consume system resources or clutter your list of containers.

### 4. Verify the Output

After the container runs, you should find two images in your current directory:

- `output_frame.jpg`: The captured frame from the YouTube live stream.
- `detected_people.jpg`: The same frame with bounding boxes drawn around detected people.

### Notes

- **Dependencies**: The Dockerfile installs `yt-dlp` for extracting the YouTube stream and `opencv-python-headless` for image processing. `FFmpeg` is used to capture frames from the video stream.
- **Adjustments**: You can modify the `-ss` parameter in the `capture_frame` function to capture a frame at a different timestamp.
- **Detection Model**: This example uses OpenCV's default HOG descriptor for people detection. For more accurate results, consider integrating a deep learning-based detector.

This setup allows you to test the entire process on your local machine using Docker, ensuring consistency and ease of deployment when you decide to move to ECS. 

## requirements:
pip install ffmpeg yt-dlp opencv-python-headless
python capture_and_detect.py


### Explanation of Key Parts:V
1. Frame Capture Over 45 Seconds: Instead of a single capture, we are capturing frames continuously and selecting the best one based on quality.
   - Stream URL Retrieval with yt-dlp: The script now retrieves the actual stream URL using yt-dlp, which should be more reliable for YouTube live videos.
   - Continuous Frame Capture: The script captures frames from the YouTube stream for 45 seconds.
   - Frame Quality Calculation: Each frame’s quality is calculated using the Laplacian variance, which is effective for detecting sharpness.
   - Best Frame Selection: The frame with the highest quality score is selected.
   - Added Error Handling: For raw image data processing to avoid errors when reshaping the array.
2. Human Detection: The selected frame is processed for human detection using OpenCV’s HOG detector.
3. Volume Mapping: Ensure that Docker has access to the correct folder on Windows.
4. Output: The final image is saved to output_image_path in Docker, showing the number of detected people and the video source URL.
5. Rebuild Docker Image: To avoid potential Docker caching issues, rebuilding without cache ensures consistency.


Further Error Handling Strategy
Network Instability: If you observe repeated No data read from FFmpeg, retrying..., the issue might be related to network instability or insufficient buffering. You could consider increasing the -rtbufsize (real-time buffer size) in FFmpeg to allow for more data buffering.

Pixel Format Compatibility: The warnings deprecated pixel format used might indicate that FFmpeg is using a format not fully compatible with OpenCV. You could specify a pixel format explicitly by adding -pix_fmt yuv420p to the ffmpeg_command to standardize it.