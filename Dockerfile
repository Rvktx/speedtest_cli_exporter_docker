FROM centos
LABEL maintainer="Mikołaj Knysak"

ENV PORT 8000
ENV SERVER 0

RUN yum install -y wget && \
    wget https://bintray.com/ookla/rhel/rpm -O bintray-ookla-rhel.repo && \
    mv bintray-ookla-rhel.repo /etc/yum.repos.d/ && \
    yum install -y speedtest python3

RUN pip3 install prometheus_client && \
    speedtest --accept-license --accept-gdpr 

EXPOSE $PORT
ADD speedtest_exporter.py /
CMD python3 ./speedtest_exporter.py --port=$PORT --server=$SERVER