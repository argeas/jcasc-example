FROM jenkins/jenkins:lts
USER root
ENV PRIVATE_KEY = '6ec8f2171591da71c90dfba20fa3300a5ce9d2f6'
ENV PUBLIC_KEY = '5cad12f837c7b8615de38a6c18e0f070'
ENV NAME keycloak-gatekeeper
ENV KEYCLOAK_VERSION 6.0.1
ENV GOOS linux
ENV GOARCH amd64

RUN apt-get update \
    && apt-get install -y \
    && apt-get -y install python3 apt-utils python3-pip \
    && pip3 install pipenv    
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
COPY jenkins.yaml /usr/share/jenkins/ref/jenkins.yaml
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt