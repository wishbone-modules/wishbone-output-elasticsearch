FROM            smetj/wishbone:latest
MAINTAINER      Jelle Smet
ARG             branch
RUN             LC_ALL=en_US.UTF-8 /usr/bin/pip3 install --process-dependency-link https://github.com/wishbone-modules/wishbone-output-elasticsearch/archive/$branch.zip
