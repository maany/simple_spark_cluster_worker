#!/bin/bash
DOCKER_RUN="sudo docker run "
for i in "$@"
do
case $i in
    --execution_id=*)
	EXECUTION_ID="${i#*=}"
	shift
	;;
	--net=*)
	NET="${i#*=}"
	shift
	;;
	-h|--help)
	echo "Usage:"
	echo "run_simple_spark_hadoop_worker.sh [--net=<overlay_network_name>] [--execution_id=<execution_id>]"
	printf "\n"
	echo "Options:"
	echo "1. net: REQUIRED; The name of the attachable overlay network to which the container should attach on startup. You should already have created an attachable overlay network on your swarm manager."
	echo "2. execution_id: REQUIRED; The execution_id representing this lightweight component in the augmented site level config file."
	exit 0
	shift
	;;
esac
done

if [ -z "$NET" ]
then
	echo "Please specify the name of the attachable docker overlay network that the container should connect to on startup."
	exit 1
fi
if [ -z "$EXECUTION_ID" ]
then
	echo "Please take a look at the augmented site level config file at the root of this directory and provide the execution id that must be deployed."
	exit 1
fi

## PRE_CONFIG EVENT ##
echo "Starting PRE_CONFIG event"
echo "Execution ID is ${EXECUTION_ID}"
docker build -t simple_spark_cluster_worker_sh_pre_config ./sh/pre_config/
docker run -it --rm -e "EXECUTION_ID=${EXECUTION_ID}" -v $(pwd)/:/component_repository simple_spark_cluster_worker_sh_pre_config bash
echo "Sourcing the environment file generated by pre_config"
source ./sh/config/run_script.env #generated by pre_config event

## CLEANUP ##
echo "Cleaning up already existing containers"
docker stop simple_spark_hadoop_worker && docker rm simple_spark_hadoop_worker

### BOOT EVENT ###
echo "Starting BOOT Event"
echo "Building image"
#build image
sudo docker build -t simple_spark_hadoop_worker sh/
echo "Building docker run command"
echo "IP = ${CONTAINER_IP}"
echo "HOST = ${CONTAINER_FQDN}"
echo "NET = ${NET}"
for NODE in ${NODES[@]}; do
	echo "NODE = $NODE"
done
DOCKER_RUN="$DOCKER_RUN -it -d"
DOCKER_RUN="$DOCKER_RUN --name ${CONTAINER_FQDN}"
DOCKER_RUN="$DOCKER_RUN --net ${NET}"
DOCKER_RUN="$DOCKER_RUN --ip ${CONTAINER_IP}"
DOCKER_RUN="$DOCKER_RUN --hostname ${CONTAINER_FQDN}"
for NODE in ${NODES[@]}; do
    DOCKER_RUN="$DOCKER_RUN --add-host ${NODE}"
done
for PORT in ${PORTS[@]}; do
    DOCKER_RUN="$DOCKER_RUN -p $PORT:$PORT"
done
DOCKER_RUN="$DOCKER_RUN --privileged"
DOCKER_RUN="$DOCKER_RUN --mount type=bind,source="$(pwd)"/sh/config,target=/etc/simple_grid/config"
DOCKER_RUN="$DOCKER_RUN -v "$(pwd)"/augmented_site_level_config_file.yaml:/etc/simple_grid/augmented_site_level_config_file.yaml"
DOCKER_RUN="$DOCKER_RUN simple_spark_hadoop_worker"

echo $DOCKER_RUN
echo "Starting container..."
$DOCKER_RUN

### INIT EVENT ######
sudo docker exec -t simple_spark_hadoop_worker /etc/simple_grid/config/init.sh
sudo docker exec -it simple_spark_hadoop_worker bash
#### POST INIT HOOKS ######