FROM ubuntu
MAINTAINER mirake mirake@docker.com

RUN apt-get update
RUN apt-get install -y vim curl wget
RUN apt-get install -y python-setuptools python-dev libmysqld-dev libmysqlclient-dev  
RUN \
    wget http://tcpdiag.dl.sourceforge.net/project/mysql-python/mysql-python-test/1.2.4b4/MySQL-python-1.2.4b4.tar.gz && \
    tar -zxvf MySQL-python-1.2.4b4.tar.gz && \
    rm -f MySQL-python-1.2.4b4.tar.gz && \
    cd MySQL-python-1.2.4b4 && \
    ln -s /usr/bin/mysql_config /usr/local/bin/mysql_config && \
    python setup.py build && \
    python setup.py install && \
    cd / && \
    rm -f -r MySQL-python-1.2.4b4
ADD server.py  /server.py
ADD run.sh  /run.sh
RUN chmod 755 /run.sh
RUN mkdir -p /app

# Define working directory.
WORKDIR /app

# Expose ports.
EXPOSE 80

# Define default command.
CMD ["/run.sh"]

