FROM jenkins/jenkins:lts
USER root
RUN apt-get update \
    && apt-get install -y \
    && apt-get -y install python3 apt-utils python3-pip \
    && pip3 install pipenv    
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
COPY jenkins.yaml /usr/share/jenkins/ref/jenkins.yaml
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt