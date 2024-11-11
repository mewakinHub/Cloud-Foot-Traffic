# Start from the official Jenkins LTS image
FROM jenkins/jenkins:lts

# Install necessary plugins by specifying them in the plugins.txt file
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugins < /usr/share/jenkins/ref/plugins.txt

# Optionally, configure Jenkins using JCasC
COPY jenkins.yaml /var/jenkins_home/jenkins.yaml

# Set environment variables for JCasC if using
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/jenkins.yaml

# Expose Jenkins ports
EXPOSE 8080 50000
