#!/bin/bash
## PRE_CONFIG EVENT ##
#docker build -t simple_spark_hadoop_worker ./sh/pre_config/
#docker stop simple_spark_hadoop_worker && docker rm simple_spark_hadoop_worker
### BOOT EVENT ###
#build image
sudo docker build -t simple_spark_hadoop_worker sh/
sudo docker run -itd \
    --name simple_spark_hadoop_worker \
    --privileged \
    -v $(pwd)/sh/config:/etc/simple_grid/config \
    -v $(pwd)/augmented_site_level_config_file.yaml:/etc/simple_grid/augmented_site_level_config_file.yaml \
    simple_spark_hadoop_worker \
#### PRE INIT HOOKS #####


### INIT EVENT ######
sudo docker exec -t simple_spark_hadoop_worker /etc/simple_grid/config/init.sh
sudo docker exec -it simple_spark_hadoop_worker bash
#### POST INIT HOOKS ######