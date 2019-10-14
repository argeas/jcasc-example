FROM jenkins/jenkins:lts
USER root
RUN apt-get update \
    && apt-get install -y \
    && apt-get -y install python3 apt-utils python3-pip \
    && pip3 install pipenv \    
    && apt-get -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget \
    && curl -O https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz \
    && tar -xf Python-3.7.3.tar.xz && cd Python-3.7.3 && ./configure --enable-optimizations && make -j 2 && make install
# WORKDIR /Python-3.7.3/    


COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
COPY jenkins.yaml /usr/share/jenkins/ref/jenkins.yaml
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt