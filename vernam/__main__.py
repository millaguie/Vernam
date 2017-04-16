# -*- coding: utf-8 -*-
import configuration
import argparse
from vernam import vernam
from cipher import xor

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                description="Vernam cipher implementation",
                add_help=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--lz4', required=False, choices=['encrypt', 'decrypt'],
                        help="Use lz4 compression while (en|de)crypting")
    group.add_argument('--base32', action='store_true', default=False,
                        help="Use base32 mode")
    group.add_argument('--raw', action='store_true', default=False,
                        help="Use raw mode (default option)")
    parser.add_argument('-i', '--inputfile', required=True,
                        help="File to encrypt or decrypt")
    parser.add_argument('-o', '--outputfile', required=True,
                        help="File to store output, stdout by default")
    parser.add_argument('-c', '--config', required=False,
                        default="config.yaml",
                        help="path to configuration file")
    parser.add_argument('-k', '--keyfile', required=False,
                        help="Path to a file containing the random data used as\
                        key for the cipher")
    parser.add_argument("-f", "--force", action='store_true', default=False,
                        help="Force to overwrite output file")
    args = parser.parse_args()

    configFromFile = configuration.readConfig(args.config)
    config = configuration.parseConfig(configFromFile, args)
    print("input file: {}, output file: {}, config file: {}, ".format(
            args.inputfile, args.outputfile, args.config)
            + "key file: {}, operation mode: {}".format(config["keyfile"],
            config["workmode"]))
    vernam(args.inputfile, config["keyfile"], args.outputfile, force=args.force,
            mode=config["workmode"])
