# Foot-Traffic detection on Cloud

### Project Structure
```
Cloud-Foot-Traffic/
│
├── Web-Dev/                        # Traditional deployment -> Always-On Server
│   ├── Front-End/                  # Front-end for traditional 1st EC2 deployment
│   │   ├── src/
│   │   ├── Dockerfile            
│   │   └── package.json
│   │
│   ├── Back-End/                   # Back-end for traditional 2nd EC2 deployment
│   │   ├── src/
│   │   ├── Dockerfile 
│   │   ├── requirements.txt
│   │   └── README.md
│   │
<!-- │   ├── docker-compose.yml              # NEEDED for cloud deployment? or just local -->
│   └── Jenkinsfile                     # CI/CD for Web-Dev (Front-End and Back-End)
│
├── AI-Server/                      # On-Demand/Serverless microservice deployment with event-driven triggers
│   ├── assets/                     # Assets for AI model or image
│   ├── configs/                    # Configuration files (e.g., RTSP sources, SAMPLING_RATE)
│   ├── outputs/                    # Output files (logs, processed data)
│   ├── src/
│   ├── Dockerfile                      # Dockerfile for packaging the serverless function
│   ├── deployment.yaml             # Optional: YAML for batch API deployment
│   ├── Jenkinsfile                     # CI/CD for serverless deployment
│   ├── requirements.txt
│   └── README.md
│
└── README.md                       # Main project README with an overview
<!-- └── notification_system/              # Notification system scripts and logic
    ├── notification_service.py       # Main script for handling notifications
    └── README.md                     # Notification system documentation -->

```
NOTE: do notification needed to be code or not?


architecture