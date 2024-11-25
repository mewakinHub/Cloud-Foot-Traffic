# Jenkins Setup for Project

This repository contains configuration files and instructions to set up Jenkins for managing CI/CD pipelines in our AWS environment.

## Website & Password [Group Project]

- **website**: http://18.142.225.7:8080
- **password**: 716e784616324eefade98c9563bfb648

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Accessing Jenkins](#accessing-jenkins)
4. [Configuration and CI/CD Best Practices](#configuration-and-cicd-best-practices)

### Prerequisites

- **AWS Environment**: Ensure you have access to the AWS account where Jenkins will be deployed.
- **Bastion Server**: Access to a bastion host is required to connect securely to Jenkins in the private subnet.
- **Private Key Files**: You’ll need the private key files (`bastionG9.pem` and `group9Key.pem`) to connect to the bastion server and the Jenkins server securely.

### Setup Instructions

1. **Clone the Repository**:

    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. **Build the Custom Jenkins Image**:

   Build the Docker image with necessary plugins and configurations.

    ```bash
    docker login -u mewakin

    docker build -t mewakin/cloud-custom-jenkins .
    docker buildx build --platform linux/arm64 -t mewakin/cloud-custom-jenkins .

    docker push mewakin/cloud-custom-jenkins
    docker pull mewakin/cloud-custom-jenkins
    ```

3. **Run the Jenkins Container with Persistent Storage**:

   Deploy Jenkins with a Docker volume for persistent storage.

    ```bash
    docker run -d -p 8080:8080 -p 50000:50000 \
        -v jenkins_home:/var/jenkins_home \
        --name jenkins-server custom-jenkins
    ```

4. **Environment Variables for AWS Credentials** (optional):

   Ensure AWS credentials or other sensitive information required for Jenkins jobs are securely set on the Jenkins server. You can do this through environment variables or the Jenkins credentials store.

### Accessing Jenkins

Since Jenkins is deployed in a private subnet, you’ll need to use the bastion server to access it.

#### 1. Connect to the Bastion Server

Use the `bastionG9.pem` key file to connect to the bastion server. Replace `<BASTION_IP>` with the IP address of the bastion server.

ssh remote with TCP protocol (allow in EC2)

```bash
ssh -i "bastion.pem" ec2-user@<BASTION_IP>
ssh -i bastion.pem ubuntu@13.213.77.92

sudo docker pull mewakin/cloud-custom-jenkins
sudo docker images ls
# sudo docker run -d -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home --name jenkins-server mewakin/cloud-custom-jenkins:latest
# Auto-Restart on Reboot
sudo docker run -d --restart unless-stopped -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home --name jenkins-server mewakin/cloud-custom-jenkins:latest
sudo docker start jenkins-server

# get password
sudo docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword

docker stop <container_name_or_id>
docker rm <container_name_or_id>
sudo docker start jenkins-server

logout
```
[website: http://<JENKINS_SERVER_IP>:8080](http://18.142.225.7:8080)
get password: 716e784616324eefade98c9563bfb648

<!-- #### 3. Access Jenkins Web Interface

- After successfully connecting to the Jenkins server, you can forward the Jenkins port to your local machine to access the web interface:
  
  ```bash
  ssh -i "group9Key.pem" -L 8080:localhost:8080 ec2-user@<JENKINS_SERVER_IP>
  ssh -i "group9Key.pem" -L 8080:localhost:8080 ubuntu@10.0.138.34
  ``` -->

- Open a browser and go to `http://localhost:8080` to access Jenkins.

### Configuration and CI/CD Best Practices

1. **Store Jenkinsfile in Source Control without Credentials**:
   - Keep the `Jenkinsfile` in your Git repository, but avoid hardcoding credentials.
   - Use Jenkins environment variables or the credentials store to handle sensitive information securely.

2. **Role-Based Access Control (RBAC)**:
   - Use Jenkins’s RBAC feature to restrict access to specific users or roles based on permissions.

3. **Set Up IAM Role for Jenkins**:
   - Create an IAM role for the Jenkins server to grant it access to AWS resources (e.g., ECR, ECS, Lambda) without embedding credentials in the codebase.
   - Attach policies for accessing only necessary resources (e.g., `AmazonEC2ContainerRegistryFullAccess`, `AmazonECSFullAccess`, `AWSLambdaExecute`).

4. **Use JCasC for Initial Configuration (Optional)**:
   - Use Jenkins Configuration as Code (JCasC) to define initial setup configurations for Jenkins, which can include plugins and credentials.

5. **Secure Jenkins Access with Bastion and SSH Keys**:
   - The Jenkins server is isolated in a private subnet for security. Always connect through the bastion host using the provided `.pem` keys.
   - Rotate SSH keys periodically and follow secure key management practices.

---
