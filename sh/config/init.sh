#!/bin/bash
echo "Copy Hadoop conf files to /root/hadoop/etc/hadoop/"
cp /etc/simple_grid/config/hadoop-env.sh /root/hadoop/etc/hadoop/
cp /etc/simple_grid/config/core-site.xml /root/hadoop/etc/hadoop/
cp /etc/simple_grid/config/hdfs-site.xml /root/hadoop/etc/hadoop/
cp /etc/simple_grid/config/mapred-site.xml /root/hadoop/etc/hadoop/
cp -f /etc/simple_grid/config/yarn-site.xml /root/hadoop/etc/hadoop/
cp -f /etc/simple_grid/config/slaves /root/hadoop/etc/hadoop/
cp -f /etc/simple_grid/config/spark-defaults.cong /root/hadoop/spark/conf/
cp -f /etc/simple_grid/config/authorized_keys ~/.ssh/authorized_keys
cat /etc/simple_grid/config/hadoop.env >> ~/.bashrc
cat /etc/simple_grid/config/hadoop-env.sh >> ~/.bashrc

echo "All Done!"

