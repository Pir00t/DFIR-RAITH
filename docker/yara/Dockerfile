# Name: DFIR-RAITH
# Description: Container build to run YaraSeeker notebook
# Author: Steven Folek | @Pir00t

FROM ubuntu:22.04
LABEL maintainer="Steven Folek | @Pir00t - <cybersecureguy@gmail.com>"

# change to root to perform updates, installs and user setup
USER root
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	git \
	sudo \
	gcc \
	curl \
	gnupg \
	ca-certificates \
	systemd \
	tree \
	python3 \
	python3-dev \
	python3-pip \
	libssl-dev \
	libffi-dev \
	libmagic-dev \
	p7zip-full && \
	apt-get upgrade -y && \
	apt-get clean && rm -rf /var/lib/apt/lists/*
	 
# NodeJS setup and install
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
ENV NODE_MAJOR=18
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update -y && apt-get install nodejs -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add analyst and group. Add workdir and tool dir, update permissions
ENV A_UID="1000" \
  A_GID="100"
  
RUN groupadd -r analyst && \
  useradd -l -m -s /bin/bash -N -u "${A_UID}" analyst && \
  mkdir -p /home/analyst/workdir && mkdir /home/analyst/tools && \
  chown -R "${A_UID}":"${A_GID}" /home/analyst 
  
# Copy & install python requirements
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Fetch and setup tools
RUN jupyter lab build

# Final var setup and command to run at start
RUN chown -R "${A_UID}":"${A_GID}" /home/analyst 
USER analyst
ENV HOME="/home/analyst" \
 PATH="$HOME/.local/bin:$PATH"
WORKDIR /home/analyst/workdir
EXPOSE 8888
CMD ["jupyter", "lab" ,"--ip=0.0.0.0" ,"--no-browser"]