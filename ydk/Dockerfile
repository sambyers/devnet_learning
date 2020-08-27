FROM ubuntu
COPY ./ydk-py-master /root/ydk-py
RUN echo 'Installing dependencies  and ydk-py'
WORKDIR /root/ydk-py
RUN /bin/bash -c './dependencies_ubuntu.sh && ./dependencies_gnmi.sh && ./tests.sh'
RUN /bin/bash -c './tests_py3.sh'