#!/bin/bash
echo "Copy Hadoop conf files to /root/hadoop/etc/hadoop/"
cp /etc/simple_grid/conf/hadoop-env.sh /root/hadoop/etc/hadoop/
cp /etc/simple_grid/conf/core-site.xml /root/hadoop/etc/hadoop/
cp /etc/simple_grid/conf/hdfs-site.xml /root/hadoop/etc/hadoop/
cp /etc/simple_grid/conf/mapred-site.xml /root/hadoop/etc/hadoop/
cp -f /etc/simple_grid/conf/yarn-site.xml /root/hadoop/etc/hadoop/
cp -f /etc/simple_grid/conf/slaves /root/hadoop/etc/hadoop/
cat hadoop.env >> ~/.bashrc
cat hadoop-env.sh >> ~/.bashrc
echo "All Done!"

