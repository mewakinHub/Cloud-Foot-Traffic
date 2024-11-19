### Decide on the Environment (Sandbox or Production)
Shotstack offers two environments:
1. **Sandbox**: For development and testing; all tasks run in a simulated environment.
2. **Production**: For live systems; tasks consume credits.

#### Best Practice:
- Use **Sandbox** for initial setup and testing.
- Switch to **Production** for live deployment.

To set the environment:
- Use the appropriate **API URL**:
  - Sandbox: `https://api.shotstack.io/stage/render`
  - Production: `https://api.shotstack.io/v1/render`

ENV: SANDBOX	
OWNER ID: ujbpso8xqf	
API KEY: pG9EMlF4g5awLHozfjyWeqzwLa6QPfG05IAHmS3u
---

### Use the Shotstack API Key
The **API Key** is all you need to authenticate requests to the Shotstack API. There’s no additional setup required in Google or other services.

#### How to Use the API Key:
1. Add it as an environment variable in your ECS task:
   - Key: `SHOTSTACK_API_KEY`
   - Value: Your API Key.
2. Reference it in your code (example in Python):
   ```python
   import os

   API_KEY = os.getenv("SHOTSTACK_API_KEY")
   API_URL = "https://api.shotstack.io/stage/render"  # Sandbox URL

   headers = {"x-api-key": API_KEY}
   ```

---

### **Step 4: Add Shotstack Integration to `model_infer` Code**

Inside `model_infer`, integrate the Shotstack frame-capture logic into your code. Here’s how you can modify your main inference script:

#### Example:
```python
import os
import requests
import time

# Get API credentials from environment variables
API_KEY = os.getenv("SHOTSTACK_API_KEY")
API_URL = os.getenv("SHOTSTACK_API_URL", "https://api.shotstack.io/stage/render")

def fetch_frames_from_youtube(youtube_url):
    payload = {
        "timeline": {
            "soundtrack": {"src": None},
            "tracks": [
                {
                    "clips": [
                        {
                            "asset": {
                                "type": "video",
                                "src": youtube_url
                            },
                            "start": 0,
                            "length": 5,
                            "fit": "cover"
                        }
                    ]
                }
            ]
        },
        "output": {
            "format": "jpg",
            "fps": 1
        }
    }

    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 201:
        job_id = response.json().get("id")
        print(f"Job submitted successfully. Job ID: {job_id}")
        return job_id
    else:
        print("Failed to submit render job")
        print(response.text)
        return None

def poll_render_status(job_id):
    headers = {"x-api-key": API_KEY}
    status_url = f"{API_URL}/{job_id}"

    while True:
        response = requests.get(status_url, headers=headers)
        status = response.json().get("status")

        if status == "done":
            print("Job completed successfully.")
            return response.json().get("url")
        elif status == "failed":
            print("Job failed.")
            return None

        time.sleep(5)

# Example Usage
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=YOUR_LIVE_STREAM_ID"
    job_id = fetch_frames_from_youtube(youtube_url)

    if job_id:
        frames_url = poll_render_status(job_id)
        if frames_url:
            print(f"Rendered frames available at: {frames_url}")
```

---

### **Step 5: Add Dockerization**
Create a `Dockerfile` in the root of `model_infer` to package the application for deployment.

#### Example Dockerfile:
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir requests

# Environment variables for Shotstack
ENV SHOTSTACK_API_URL=https://api.shotstack.io/stage/render
ENV SHOTSTACK_API_KEY=your_api_key_here

# Command to run the application
CMD ["python", "your_script.py"]
```

---

### **Step 6: Test Locally**
1. Build the Docker image:
   ```bash
   docker build -t model_infer .
   ```
2. Run the container locally:
   ```bash
   docker run -e SHOTSTACK_API_KEY=your_api_key_here model_infer
   ```

---

### **Step 7: Deploy to AWS ECS**

#### Steps:
1. **Push the Docker Image**:
   - Tag and push your Docker image to **AWS Elastic Container Registry (ECR)**:
     ```bash
     docker tag model_infer <your_ecr_repository_uri>
     docker push <your_ecr_repository_uri>
     ```

2. **Create ECS Task Definition**:
   - Go to the ECS dashboard.
   - Create a new task definition and set the container image to your ECR repository.
   - Add environment variables:
     - `SHOTSTACK_API_KEY`: Your API key.
     - `SHOTSTACK_API_URL`: `https://api.shotstack.io/stage/render` (or production URL).

3. **Run the Task**:
   - Create an ECS service or trigger the task ad hoc.

4. **Networking**:
   - Ensure the task has internet access via a NAT Gateway or public subnet.

---

### **Step 8: Monitor and Validate**
1. **CloudWatch Logs**:
   - Check ECS logs to verify that the API integration is working.
2. **Shotstack Dashboard**:
   - Monitor submitted jobs and check for successful frame captures.

---

### **Final Notes**
- Start in **Sandbox** mode to avoid consuming production credits during testing.
- Ensure your ECS container has sufficient IAM permissions for logging and internet access.

Would you like help setting up the ECS environment or validating the Shotstack integration?