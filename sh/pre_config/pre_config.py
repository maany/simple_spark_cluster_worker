import argparse
import yaml
import dicttoxml
from xml.dom.minidom import parseString


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site_config', help="Compiled Site Level Configuration YAML file")
    parser.add_argument('--execution_id', help="ID of lightweight component")
    parser.add_argument('--output_dir', help="Output directory")
    args = parser.parse_args()
    return {
        'augmented_site_level_config_file': args.site_config,
        'execution_id': args.execution_id,
        'output_dir': args.output_dir
    }


def get_current_lightweight_component(data, execution_id):
    current_lightweight_component = None
    for lightweight_component in data['lightweight_components']:
        if lightweight_component['execution_id'] == int(execution_id):
            current_lightweight_component = lightweight_component
            break
    return current_lightweight_component


def generate_xml(properties, root="configuration", xml_headers=None):
    if xml_headers is None:
        xml_headers = [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            "<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>"
        ]
    xml_headers_string = '\n'.join(xml_headers)
    xml_content = []
    for property in properties:
        xml_content.append({
            "property": property
        })
    xml_string = parseString(dicttoxml.dicttoxml(xml_content,
                                                 custom_root=root,
                                                 attr_type=False,
                                                 item_func=lambda x: None).replace('<None>', '').replace('</None>', '')).toprettyxml()
    xml_content = xml_string.split('\n')
    xml_string = '\n'.join(xml_content[1:])
    output = "{xml_headers_string}\n{xml_string}".format(xml_headers_string=xml_headers_string, xml_string=xml_string)
    return output


def get_core_site_xml_content(data, execution_id):
    current_lightweight_component = get_current_lightweight_component(data, execution_id)
    config = current_lightweight_component['config']
    properties = []

    fs_default_name_property = {
            "name": "fs.default.name",
            "value": "hdfs://{fs_default_name}:9000".format(fs_default_name=config['fs_default_name'])
        }
    properties.append(fs_default_name_property)
    output = generate_xml(properties)
    return output


def get_hdfs_site_xml_content(data, execution_id):
    current_lightweight_component = get_current_lightweight_component(data, execution_id)
    config = current_lightweight_component['config']
    properties = []

    dfs_namenode_name_dir_property = {
        "name": "dfs.namenode.name.dir",
        "value": "/root/data/nameNode"
    }

    dfs_datanode_data_dir = {
        "name": "dfs.datanode.data.dir",
        "value": "/root/data/dataNode"
    }

    dfs_replication_property = {
        "name": "dfs.replication",
        "value": config['hdfs_dfs_replication']
    }
    properties.extend([dfs_datanode_data_dir, dfs_namenode_name_dir_property, dfs_replication_property])
    output = generate_xml(properties)
    return output


def get_mapred_site_xml_content(data, execution_id):
    current_lightweight_component = get_current_lightweight_component(data, execution_id)
    config = current_lightweight_component['config']
    properties = []

    mapreduce_framework_name = {
        "name": "mapreduce.framework.name",
        "value": "yarn"
    }

    yarn_app_mapreduce_am_resource_mb = {
        "name": "yarn.app.mapreduce.am.resource.mb",
        "value": config['yarn_app_mapreduce_am_resource_mb']
    }

    mapreduce_map_memory_mb = {
        "name": "mapreduce.map.memory.mb",
        "value": config['mapreduce_map_memory_mb']
    }

    mapreduce_reduce_memory_mb = {
        "name": "mapreduce.reduce.memory.mb",
        "value": config["mapreduce_reduce_memory_mb"]
    }
    properties.extend([mapreduce_framework_name, yarn_app_mapreduce_am_resource_mb, mapreduce_map_memory_mb, mapreduce_reduce_memory_mb])
    output = generate_xml(properties)
    return output


def get_yarn_site_xml_content(data, execution_id):
    current_lightweight_component = get_current_lightweight_component(data, execution_id)
    config = current_lightweight_component['config']
    properties = []

    yarn_acl_enable = {
        "name": "yarn.acl.enable",
        "value": 0
    }

    yarn_resourcemanager_hostname = {
        "name": "yarn.resourcemanager.hostname",
        "value": config['yarn_resource_manager_hostname']
    }

    yarn_nodemanager_aux_services = {
        "name": "yarn.nodemanager.aux-services",
        "value": "mapreduce_shuffle"
    }

    yarn_nodemanager_resource_memory_mb = {
        "name": "yarn.nodemanager.resource.memory-mb",
        "value": config['yarn_nodemanager_resource_memory_mb']
    }

    yarn_scheduler_maximum_allocation_mb = {
        "name": "yarn.scheduler.maximum-allocation-mb",
        "value": config["yarn_scheduler_maximum_allocation_mb"]
    }

    yarn_scheduler_minimum_allocation_mb = {
        "name": "yarn.scheduler.minimum-allocation-mb",
        "value": config["yarn_scheduler_minimum_allocation_mb"]
    }

    yarn_nodemanager_vmem_check_enabled = {
        "name": "yarn.nodemanager.vmem-check-enabled",
        "value": "false"
    }
    properties.extend([yarn_acl_enable,
                       yarn_resourcemanager_hostname,
                       yarn_nodemanager_aux_services,
                       yarn_nodemanager_resource_memory_mb,
                       yarn_scheduler_maximum_allocation_mb,
                       yarn_scheduler_minimum_allocation_mb,
                       yarn_nodemanager_vmem_check_enabled])
    output = generate_xml(properties)
    return output


def get_hadoop_env_sh_file_content():
    env = ["export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.201.b09-2.el7_6.x86_64/jre"]
    return '\n'.join(env)


def get_hadoop_env_file_content():
    env = ["JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.201.b09-2.el7_6.x86_64/jre",
           "PATH=/root/hadoop/spark/bin:/root/hadoop/bin:/root/hadoop/sbin:/usr/sue/sbin:/usr/sue/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
           "HADOOP_CONF_DIR=/root/hadoop/etc/hadoop", "SPARK_HOME=/root/hadoop/spark",
           "LD_LIBRARY_PATH=/root/hadoop/lib/native:$LD_LIBRARY_PATH"]
    return '\n'.join(env)


def get_slaves_file_content(data, execution_id):
    slaves_execution_id = []
    slaves = []
    for lightweight_component in data['lightweight_components']:
        if lightweight_component['type'] == "spark_hadoop_worker":
            slaves_execution_id.append(lightweight_component['execution_id'])

    for execution_id in slaves_execution_id:
        for dns_info in data['dns']:
            if dns_info['execution_id'] == execution_id:
                slaves.append(dns_info['container_fqdn'])
    return '\n'.join(slaves)


def get_spark_defaults_conf_content(data, execution_id):
    current_lightweight_component = get_current_lightweight_component(data, execution_id)
    config_section = current_lightweight_component['config']
    config = []
    config.append("spark.master {value}".format(value=str("yarn").lower()))
    spark_event_log_enabled = config_section['spark_event_log_enabled']
    config.append("spark.event.log.enabled {value}".format(value=str(spark_event_log_enabled).lower()))
    spark_event_log_dir = config_section['spark_event_log_dir']
    config.append("spark.event.log.dir {value}".format(value=str(spark_event_log_dir).lower()))
    spark_driver_memory = config_section['spark_driver_memory']
    config.append("spark.driver.memory {value}".format(value=str(spark_driver_memory).lower()))
    spark_yarn_am_memory = config_section['spark_yarn_am_memory']
    config.append("spark.yarn.am.memory {value}".format(value=str(spark_yarn_am_memory).lower()))
    spark_executor_memory = config_section['spark_executor_memory']
    config.append("spark.executor.memory {value}".format(value=str(spark_executor_memory).lower()))
    config.append(
        "spark.history.provider {value}".format(value=str("org.apache.spark.deploy.history.FsHistoryProvider")))
    spark_history_fs_log_directory = config_section['spark_history_fs_log_directory']
    for dns_info in data['dns']:
        if dns_info['type'] == 'spark_hadoop_master':
            hdfs_master=dns_info['container_fqdn']
            break
    config.append("spark.history.fs.logDirectory hdfs://{hdfs_master}:9000/{value}".format(hdfs_master=hdfs_master, value=str(spark_history_fs_log_directory).lower()))
    spark_history_fs_update_interval = config_section['spark_history_fs_update_interval']
    config.append(
        "spark.history.fs.update.interval {value}".format(value=str(spark_history_fs_update_interval).lower()))
    config.append("spark.history.ui.port {value}".format(value=str("18080").lower()))
    return "\n".join(config)


if __name__ == "__main__":
    args = parse_args()
    execution_id = args['execution_id']
    site_config_filename =  args['augmented_site_level_config_file']
    site_config = open(site_config_filename, 'r')
    data = yaml.load(site_config)
    output_dir = args['output_dir']
    with open("{output_dir}/core-site.xml".format(output_dir=output_dir), 'w') as core_site:
        core_site.write(get_core_site_xml_content(data, execution_id))

    with open("{output_dir}/hdfs-site.xml".format(output_dir=output_dir), 'w') as hdfs_site:
        hdfs_site.write(get_hdfs_site_xml_content(data, execution_id))

    with open("{output_dir}/mapred-site.xml".format(output_dir=output_dir), 'w') as mapred_site:
        mapred_site.write(get_mapred_site_xml_content(data, execution_id))

    with open("{output_dir}/yarn-site.xml".format(output_dir=output_dir), 'w') as yarn_site:
        yarn_site.write(get_yarn_site_xml_content(data, execution_id))

    with open("{output_dir}/hadoop-env.sh".format(output_dir=output_dir), 'w') as hadoop_env:
        hadoop_env.write(get_hadoop_env_sh_file_content())

    with open("{output_dir}/hadoop.env".format(output_dir=output_dir), 'w') as hadoop_env:
        hadoop_env.write(get_hadoop_env_file_content())

    with open("{output_dir}/slaves".format(output_dir=output_dir), 'w') as slaves:
        slaves.write(get_slaves_file_content(data))

    with open("{output_dir}/spark-defaults.conf".format(output_dir=output_dir), 'w') as slaves:
        slaves.write(get_spark_defaults_conf_content(data))

    # with open("{output_dir}/known_hosts".format(output_dir=output_dir), 'w') as known_hosts:
    #     slaves.write(get_known_hosts_content(data, execution_id))
