# -*- coding: utf-8 -*-
import configuration
import argparse
from cipher import xor

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                description="Vernam cipher implementation",
                add_help=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--encrypt',
                        help="Encryption mode")
    group.add_argument('-d', '--decrypt',
                        help="Decryption mode")
    parser.add_argument('-i', '--inputfile', required=True,
                        help="File to encrypt or decrypt")
    parser.add_argument('-o', '--outputfile', required=False, default="stdout",
                        help="File to store output, stdout by default")
    parser.add_argument('-c', '--config', required=False,
                        default="config.yaml",
                        help="path to configuration file")
    parser.add_argument('-k', '--keyfile', required=False,
                        help="Path to a file containing the random data used as\
                        key for the cipher")
    parser.add_argument("-m", "--workmode", required=False,
                        choices=["lz4", "base32", "raw"],
                        help="Choose an optimization (lz4, base32 or raw)")
    args = parser.parse_args()

    configFromFile = configuration.readConfig(args.config)
    config = configuration.parseConfig(configFromFile, args)
    print("mode: {}, input file: {}, output file: {}, config file: {}, \
            key file: {}, operation mode: {}".format(config["mode"], args.inputfile,
            args.outputfile, args.config, config["keyfile"], config["workmode"] ))
