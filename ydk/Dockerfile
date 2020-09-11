# https://github.com/CiscoDevNet/ydk-py
# A docker image is automatically built with the latest ydk-py installed.
FROM ydkdev/ydk-py

COPY . /root/my-ydk

WORKDIR /root/my-ydk

RUN ["python3", "ydk-example-1.py"]