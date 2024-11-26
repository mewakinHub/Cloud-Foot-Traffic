## Manual
1. zip folder and CICD to Lambda
2. add Trigger (EventBridge)
- create a new rule
- Schedule expression
    ```
    cron(0/1 * * * ? *) # 1 minute
    cron(0 0/1 * * ? *) # 1 hour
    cron(0 0 * * ? *)   # 1 day
    ```
- Monitor tabs -> view cloudwatch log

## Local Access
1. open tunnel for access in local device
ssh -i bastionG9.pem -L 3307:mysql-rds-g09.cbk2ewumyiw9.ap-southeast-1.rds.amazonaws.com:3306 ubuntu@54.169.55.224
2. download workbench for manipulate db with UI-based

Here's a refined and structured approach for setting up the payload and data flow for your ECS Fargate batch processing, including notifications and logging for anomaly detection:


---

### Payload Flow

#### 1. API Gateway (for EC2 Ad-Hoc Trigger)
When an EC2 instance initiates an ad-hoc request, it sends a payload to the Lambda Controller via API Gateway.

##### Payload Structure (API Gateway to Lambda Controller):
```json
{
  "source": "API_GATEWAY",
  "user_id": "user_1",
  "streaming_URL": "https://example.com/stream",
  "email": "user@example.com",
  "Monitoring_status": true
}
```

This payload will trigger processing specifically for `user_1`.

---

#### 2. EventBridge (for Scheduled Trigger)
EventBridge triggers batch processing every hour, checking all users in the `config` table with `Monitoring_status: true`.

##### Payload Structure (EventBridge to Lambda Controller):
```json
{
  "source": "EVENTBRIDGE",
  "users": [
    {
      "user_id": "user_1",
      "streaming_URL": "https://example.com/stream1",
      "email": "user1@example.com",
      "Monitoring_status": true
    },
    {
      "user_id": "user_2",
      "streaming_URL": "https://example.com/stream2",
      "email": "user2@example.com",
      "Monitoring_status": true
    }
    // Additional users
  ]
}
```

This batch payload processes all users with `Monitoring_status: true`.

---

### Lambda Controller Workflow

1. **Source Identification**:
   - Checks if `source` is `API_GATEWAY` or `EVENTBRIDGE`.
   - If `API_GATEWAY`, it processes a single user payload.
   - If `EVENTBRIDGE`, it processes a batch of users.

2. **Payload Preparation for ECS Fargate**:
   - For each user in the payload (either single or batch), prepare a sub-payload for ECS.
   - Include necessary fields: `user_id`, `streaming_URL`, and `email`.

##### Payload to ECS Fargate:
```json
{
  "user_id": "user_1",
  "streaming_URL": "https://example.com/stream",
  "email": "user@example.com"
}
```

3. **Trigger ECS Task**:
   - For each sub-payload, trigger an ECS Fargate task.

---

### ECS Fargate: youtube-detection-app

1. **Process the Stream**:
   - Using `streaming_URL`, retrieve frames, perform object detection, and annotate the image.
   - Count the number of people detected.

2. **Prepare Result**:
   - If `result` exceeds threshold (e.g., 15 people), flag for notification.
   - Save the `processed_detection_image` as Base64.
   - Generate a result object.

3. **Result Handling Based on Source**:
   - **EventBridge**: Save results to `result` table in RDS, append record to `{user_id}.csv` in S3, and log in CloudWatch.
   - **API Gateway**: Send the result back to the initiating EC2 instance through a FastAPI POST request.

##### Result Payload (from ECS to Lambda Notification):
For flagged events (e.g., more than 15 people detected), ECS sends a payload to the Lambda Notification function:
```json
{
  "user_id": "user_1",
  "DATE-TIME": "2024-01-01T12:00:00Z",
  "config": {
    "Monitoring_status": true,
    "streaming_URL": "https://example.com/stream",
    "email": "user@example.com"
  },
  "result": {
    "people_count": 20
  },
  "processed_detection_image": "base64_encoded_image_data"
}
```

### Lambda Notification Workflow

1. **Analyze Result**:
   - If `people_count` exceeds threshold (e.g., 15 people), convert `processed_detection_image` to `.jpg` and save in S3.

2. **Send Notification**:
   - Use SNS to email the user the result, including image and count.

---

### Summary of Data Flow

1. **API Gateway or EventBridge → Lambda Controller**:
   - Prepares and sends payloads to ECS Fargate.

2. **ECS Fargate**:
   - Processes video, performs detection, and prepares results.
   - Saves results to RDS, appends to S3, and logs in CloudWatch.
   - Sends flagged results to Lambda Notification.

3. **Lambda Notification**:
   - Sends alert to user via SNS email if foot traffic threshold is exceeded.


### Considerations and Enhancements

1. **Concurrency Handling**:
   - Use separate Fargate tasks to avoid conflict between EventBridge and API Gateway triggers.

2. **Resource Management**:
   - Adjust ECS task definitions to scale with load, especially for API Gateway, where ad-hoc requests may require faster scaling.

3. **Error Handling and Logging**:
   - Integrate CloudWatch for logging errors or anomalies (e.g., video stream errors, processing delays).
   - Use retries and error notifications if any ECS task fails or RDS/S3 operations have issues.

4. **Data Retention**:
   - Implement lifecycle policies for S3 data retention based on user requirements (e.g., store images for a year).

This setup ensures flexible handling of batch and ad-hoc processing requests, supports efficient scaling, and provides alert mechanisms for unusual activity.