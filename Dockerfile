FROM alpine:3.10.3
MAINTAINER Your boy Chris

RUN apk update

RUN apk add python
RUN apk add py-pip
RUN pip install schedule
RUN pip install slackclient
RUN apk add wget
RUN apk add unzip


RUN wget https://releases.hashicorp.com/terraform/0.12.13/terraform_0.12.13_linux_amd64.zip
RUN unzip terraform_0.12.13_linux_amd64.zip
RUN mv terraform /usr/bin

### Install dvpn community ed
RUN wget https://github.com/vfanu/dragonvpn-community-Infra/archive/master.zip
RUN unzip master.zip

RUN mv dragonvpn-community-Infra-master /dragon_vpn

RUN mkdir /python

#### COPY THE APP CODE ####
COPY startup.sh /python
COPY vpnbot.py /python
COPY aws_region_finder.py /python
COPY response_generator.py /python
COPY slack_messenger.py /python

RUN chmod +x /python/startup.sh

ENTRYPOINT ["/python/startup.sh"]
