# Jenkins Setup for Project

This repository contains configuration files and instructions to set up Jenkins for managing CI/CD pipelines in our AWS environment.

## Website & Password [Group Project]

- **website**: http://13.215.174.242:8080/
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

### Deploying in Jenkins's dedicated EC2

Since Jenkins is deployed in a private subnet, you’ll need to use the bastion server to access it.

#### Connect to the Bastion Server

Use the `bastionG9.pem` key file to connect to the bastion server. Replace `<BASTION_IP>` with the IP address of the bastion server.

ssh remote with TCP protocol (allow in EC2)

```bash
<<<<<<< HEAD
ssh -i "bastionG9.pem" ec2-user@<BASTION_IP>
ssh -i bastion.pem ubuntu@54.81.57.229

scp -i "group9Key.pem" /path/on/bastion/file ec2-user@<JENKINS_SERVER_IP>:/path/on/jenkins-server/
scp -i group9Key.pem group9Key.pem ubuntu@54.169.55.224:/ubuntu/home (from local terminal)
```

<!-- #### 2. SSH into the Jenkins Server via Bastion

Once on the bastion server, use the `group9Key.pem` key file to access the Jenkins server.

```bash
ssh -i "group9Key.pem" ec2-user@<JENKINS_SERVER_IP>
ssh -i "group9Key.pem" ubuntu@10.0.138.34 -->
=======
ssh -i "bastion.pem" ec2-user@<BASTION_IP>
ssh -i bastion.pem ubuntu@13.215.174.242
>>>>>>> 2c6f614087da2d05a173c5e2126874612c112695

```
sudo docker pull mewakin/cloud-custom-jenkins
sudo docker images ls
sudo docker images
<<<<<<< HEAD

docker stop <container_name_or_id>
docker rm <container_name_or_id>
logout
=======
>>>>>>> 2c6f614087da2d05a173c5e2126874612c112695

# Auto-Restart on Reboot
docker run -d \
  --name jenkins-server \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  mewakin/cloud-custom-jenkins:latest

# get password
sudo docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword

docker exec -u root -it jenkins-server bash
chown root:docker /var/run/docker.sock
chmod 660 /var/run/docker.sock
exit

sudo docker restart jenkins-server

docker exec -it jenkins-server bash
groups
docker ps
ls -la /var/run/docker.sock

docker stop jenkins-server
docker rm jenkins-server
sudo docker start jenkins-server

logout
```
<<<<<<< HEAD
[website: http://<JENKINS_SERVER_IP>:8080](http://54.81.57.229:8080)
get password: [716e784616324eefade98c9563bfb648](http://54.81.57.229:8080)
=======
- Open a browser and go to [website: http://<JENKINS_SERVER_IP>:8080](http://13.215.174.242:8080)
get password: 73f83a28a23c4379857265e3e7d4648a
>>>>>>> 2c6f614087da2d05a173c5e2126874612c112695

#### set-up UI-based browser Jenkins Wizard

username: admin
password: admin

docker restart <CONTAINER_NAME_OR_ID>
sudo apt install -y openjdk-11-jdk

1. **Add a `tests/` Directory**:
   - Place the Robot Framework test cases in a dedicated `tests/` folder within each microservice directory (e.g., `microservices/model_inference/tests/`).
   - Structure the tests using a modular approach:
     - `test_model_inference.robot`: Main test suite for `model_inference`.
     - `resources/`: Shared keywords for reusability across test cases.
     - `variables/`: Reusable variables for maintaining test configuration.

2. **Update the `Jenkinsfile` in `model_inference`**:
   Modify the CI/CD pipeline to include a testing stage for Robot Framework. Example:
   ```groovy
   pipeline {
       agent any
       stages {
           stage('Build Docker Image') {
               steps {
                   sh 'docker build -t model_inference .'
               }
           }
           stage('Run Tests') {
               steps {
                   sh 'docker run --rm -v $(pwd)/output:/tests/output model_inference robot --outputdir /tests/output tests/'
               }
           }
           stage('Push to ECR') {
               steps {
                   sh '''
                   $(aws ecr get-login --no-include-email --region us-east-1)
                   docker tag model_inference:latest <your-ecr-repo>:latest
                   docker push <your-ecr-repo>:latest
                   '''
               }
           }
       }
   }
   ```

3. **Integrate Robot Framework into Docker**:
   - Update the `Dockerfile` in `model_inference` to include Robot Framework and dependencies:
     ```dockerfile
     FROM python:3.9-slim
     RUN apt-get update && apt-get install -y curl xvfb firefox-esr && rm -rf /var/lib/apt/lists/*
     RUN pip install --no-cache-dir robotframework robotframework-seleniumlibrary selenium
     WORKDIR /tests
     COPY . /tests
     ENTRYPOINT ["robot", "--outputdir", "/tests/output"]
     ```

---

##### Workflow for Robot Framework Integration:
1. **Development**:
   - Write and test your Robot Framework scripts locally within `tests/`.
   - Use `resources/` and `variables/` directories for reusable components.

2. **Testing in CI/CD**:
   - During the Jenkins pipeline execution:
     1. Build the `model_inference` Docker image.
     2. Run the Robot Framework tests in a containerized environment.
     3. Generate test reports in the `output/` directory.

3. **Deployment**:
   - If tests pass, push the Docker image to ECR.
   - ECS tasks automatically pull the updated image and deploy the new service.
