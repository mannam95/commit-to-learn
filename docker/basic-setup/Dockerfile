# pull a base ubuntu image
FROM ubuntu:latest

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y
RUN apt-get upgrade -y

# Install some basic tools
RUN apt-get install -y software-properties-common

# Install some basic tools
RUN apt-get install -y vim nano less

# Once the container is created, run the following commands
CMD ["/bin/bash"]