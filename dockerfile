#Base ของ image ให้เลือกใช้ให้ตรงกับ version cuda ในเครื่องของท่าน
FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /ML_proc

COPY requirements.txt .
COPY . .

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.8 python3-pip

RUN apt-get install -y ffmpeg
RUN apt install nano
RUN apt-get install -y python3.8-distutils
RUN python3.8 -m pip install -r requirements.txt
EXPOSE 8082                                                                                                         