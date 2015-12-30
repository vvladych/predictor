import os
import configparser
import logging

try:
    from predictor.helpers.CONST import CONST
    CONFIG_DIR = CONST.CONFIG_DIR
except:
    CONFIG_DIR = "config"


def discover_config(package_name):
    config_base_name = os.path.basename(package_name).split('.')[0]
    config_file_name = """config.%s.conf""" % (config_base_name)
    return config_file_name


def read_config(package_name):
    config_file_name = discover_config(package_name)
    config = configparser.ConfigParser()
    full_config_file_name = """%s/%s""" % (CONFIG_DIR, config_file_name)
    if os.path.exists(os.path.realpath(full_config_file_name)):
        config.read(os.path.realpath(full_config_file_name))
        logging.warning("full_config_file %s successful readed" % full_config_file_name)
    else:
        logging.warning("full_config_file_name %s is not in path" % os.path.realpath(full_config_file_name))
    return config
