FROM ubuntu
MAINTAINER jnory <jnory@alpacadb.com>

RUN apt-get update

# pip and fabric
RUN apt-get install -y python-pip
RUN apt-get install -y python-dev
RUN pip install fabric

ADD fabfile.py /opt/
RUN cd /opt && fab local_deploy

