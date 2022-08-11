FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y curl
RUN curl -O http://launchpadlibrarian.net/598553093/mysql-server-5.7_5.7.38-0ubuntu0.18.04.1_arm64.deb
RUN apt install -y ./mysql-server-5.7_5.7.38-0ubuntu0.18.04.1_arm64.deb

#ENTRYPOINT ["/bin/sh","-c","service mysql start && tail -f /var/log/mysql/error.log"]

EXPOSE 3306

