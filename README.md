# Foot-Traffic detection on Cloud

NOTE: do notification needed to be code or not?


### Project Structure
``` 
Cloud-Foot-Traffic/
├── web-app/
│   ├── front-end/
│   │   ├── Dockerfile
│   │   ├── src/
│   ├── back-end/
│   │   ├── Dockerfile
│   │   └── src/
│   └── nginx/                  # for load balancer and proxy
│       ├── Dockerfile
│       └── nginx.conf
│   ├── docker-compose.yml      # Docker Compose file for nginx
│   └── Jenkinsfile             # CI/CD pipeline for both front-end and back-end
├── microservices/
│   ├── model_inference/
│   │   ├── Dockerfile
│   │   ├── src/
│   │   ├── requirements.txt
│   │   └── Jenkinsfile         # CI/CD pipeline for Fargate deployment
│   └── controller/
│       ├── src/
│       ├── requirements.txt
│       ├── Dockerfile          # optional: we can zipped instead of building the image
│       └── Jenkinsfile         # CI/CD pipeline for Lambda deployment
├── IaC/
│   ├── deployment.yaml
│   ├── eventbridge.yaml
│   └── Jenkinsfile             # CI/CD for IaC deployments
├── jenkins/
│   ├── Dockerfile     # Dockerfile for Jenkins container (create volume for UI based cache)
│   ├── README.md      # Step for build and deploy into dedicated EC2 instance
│   └── jenkins.yaml   # Jenkins Configuration as Code (JCasC)
└── README.md
```