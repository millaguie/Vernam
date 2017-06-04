# -*- coding: utf-8 -*-
"""
This class is intended for configuration management
"""
import os
import sys
import yaml

def readConfig(config):
    """
    This function reads configuration file and combine it with parameters from
    console input to generate the configuration list.
      Parameters
    -----------
    config: configuration file to be readed

     options
    ----------
    keyfile (-k) : str, path to a file containing the random data used as key
        for the cipher.
    workmode     :  You can choose one of the following methods:
        lz4 : Will compress input or decompres output with lz4, this has a great
            performance with all file types.
        base32 : Old style. key will be read as 4 bits blocks, input and output
            will use  RFC 4648 Base 32 encoding. This is useful when one of
            the sides is doing the maths by hand.
        raw  : default operation mode, will use 1KB pages for ciphering
    """
    if not os.path.exists(config):
        sys.stderr.write("Could not find config file, "
                         +"creating a default one\n")
        configFile = open(config, "w")
        configFile.write("---\nkeyfile: defaultrawfile.rnd\nworkmode: raw")
        configFile.close()
    return yaml.load(open(config, 'r'))

def parseConfig(configFromFile, configFromCmd, mode="raw"):
    """
    This fuction merges configuration from config file and configuration from
    command line. Command line options have preference over config file.

     Parameters
    -----------
    configFromFile  :  returned from readConfig functions
    configFromCmd   :  args from command line
    mode            :  parse mode option
    """
    conf = {}
    if mode is "lz4":
        conf["workmode"] = "lz4"
        print("mode lz4")
    elif mode is "base32":
        conf["workmode"] = "base32"
    elif mode is "human":
        conf["workmode"] = "human"
    elif configFromFile['workmode'] is not None:
        conf["workmode"] = configFromFile['workmode']
    else:
        conf["workmode"] = "raw"

    conf["keyfile"] = configFromCmd.keyfile or configFromFile['keyfile']
    return conf
