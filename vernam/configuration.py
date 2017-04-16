# -*- coding: utf-8 -*-
import yaml
import os
import sys

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
    workmode (-m) :  You can choose one of the following methods:
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
    return yaml.load(open(config,'r'))

def parseConfig(configFromFile, configFromCmd):
    """
    This fuction merges configuration from config file and configuration from
    command line. Command line options have preference over config file.

     Parameters
    -----------
    configFromFile  :  returned from readConfig functions
    configFromCmd   :  args from command line
    """
    conf = {}
    if 'encrypt' in locals():
        conf["mode"] = "encrypt"
    else:
        conf["mode"] ="decrypt"
    conf["keyfile"] = configFromCmd.keyfile or configFromFile['keyfile']
    conf["workmode"] = configFromCmd.workmode or configFromFile['workmode']
    return conf
