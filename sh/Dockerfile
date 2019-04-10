FROM cern/cc7-base
LABEL Maintainer="Mayank Sharma (imptodefeat@gmail.com)"

WORKDIR /root/
# Install Java
RUN yum install -y java-1.8.0-openjdk-headless \
    java-1.8.0-openjdk-devel

# Install Hadoop
RUN yum install -y wget vim
RUN wget https://www-eu.apache.org/dist/hadoop/common/hadoop-2.8.5/hadoop-2.8.5.tar.gz && tar -xzf hadoop-2.8.5.tar.gz && mv hadoop-2.8.5 hadoop

# Install Spark
RUN wget https://www-eu.apache.org/dist/spark/spark-2.4.1/spark-2.4.1-bin-hadoop2.7.tgz && \
    tar -xzf /root/spark-2.4.1-bin-hadoop2.7.tgz --directory /root/hadoop/ &&\
    mv /root/hadoop/spark-2.4.1-bin-hadoop2.7 /root/hadoop/spark

# ssh and net-tools
RUN yum -y install iproute openssh openssh-server openssh-clients openssl-libs net-tools;yum clean all;
RUN mkdir /root/.ssh && chmod 700 /root/.ssh
COPY ./data/authorized_keys /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN ssh-keygen -A

# Config Hadoop
RUN mkdir -p /etc/hadoop/conf && mkdir /root/data

# systemd
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]
