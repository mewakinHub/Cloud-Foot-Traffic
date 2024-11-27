# Start from the official Jenkins LTS image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install Docker CLI
RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*

# Install necessary plugins and configuration
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugins < /usr/share/jenkins/ref/plugins.txt

COPY jenkins.yaml /var/jenkins_home/jenkins.yaml

# Ensure Jenkins user has permissions to use Docker
RUN usermod -aG docker jenkins

# Switch back to Jenkins user
USER jenkins

# Expose Jenkins ports
EXPOSE 8080 50000
