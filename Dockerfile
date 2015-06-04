FROM ubuntu
MAINTAINER jnory <jnory@alpacadb.com>

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y build-essential
RUN apt-get install -y git
RUN apt-get install -y wget
RUN apt-get install -y libjpeg-dev libblas-dev libatlas-dev libatlas-base-dev liblapack-dev gfortran
RUN apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev
RUN apt-get install -y libhdf5-serial-dev bc libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler

# python libs
RUN apt-get install -y python-numpy python-scipy
RUN apt-get install -y python-pip
RUN apt-get install -y python-dev
RUN pip install fabric
RUN pip install six

# download cuda
RUN mkdir -p /opt/archives
RUN cd /opt/archives && wget http://developer.download.nvidia.com/compute/cuda/7_0/Prod/local_installers/cuda_7.0.28_linux.run

ADD fabfile.py /opt/
RUN cd /opt && fab local_deploy

