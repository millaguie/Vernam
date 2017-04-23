# -*- coding: utf-8 -*-
import configuration
import argparse
from vernam import vernam
from cipher import xor

if __name__ == '__main__':

    #Parse all arguments from command line
    parser = argparse.ArgumentParser(
                description="Vernam cipher implementation",
                add_help=True)

    # App can perform one action a time
    actionGr = parser.add_mutually_exclusive_group()
    actionGr.add_argument('-e', '--encrypt', required=False,
                        action='store_true', help="Start in encryption mode")
    actionGr.add_argument('-d', '--decrypt', required=False,
                        action='store_true', help="Start in decryption mode")
    actionGr.add_argument('--catalog', required=False, action='store_true',
                        help="Catalog a new keyfile")

    # encrypt or decryption can operate in one mode but only one
    modeGr = parser.add_mutually_exclusive_group()
    modeGr.add_argument('--lz4', action='store_true', default=False,
                        help="Use lz4 compression mode")
    modeGr.add_argument('--base32', action='store_true', default=False,
                        help="Use base32 mode")
    modeGr.add_argument('--raw', action='store_true', default=False,
                        help="Use raw mode (default option)")

    #All other stuff
    parser.add_argument('-i', '--inputfile', required=True,
                        help="File to encrypt or decrypt, when using in catalog\
                        mode keyfile to catalog")
    parser.add_argument('-o', '--outputfile', required=False,
                        help="File to store output, stdout by default")
    parser.add_argument('-c', '--config', required=False,
                        default="config.yaml",
                        help="Path to configuration file")
    parser.add_argument('-k', '--keyfile', required=False,
                        help="Path to a file containing the random data used "+
                        "as key for the cipher")
    parser.add_argument("-f", "--force", action='store_true', default=False,
                        help="Force to overwrite output file")
    args = parser.parse_args()


    # Read configuration file
    configFromFile = configuration.readConfig(args.config)

    # merge configuration from command line and config file
    config = configuration.parseConfig(configFromFile, args)
    print("input file: {}, output file: {}, config file: {}, ".format(
            args.inputfile, args.outputfile, args.config)
            + "key file: {}, operation mode: {}".format(config["keyfile"],
            config["workmode"]))
    if args.encrypt is True or args.encrypt is True:
        vernam(args.inputfile, config["keyfile"], args.outputfile,
            force=args.force, mode=config["workmode"])
    elif args.catalog is True:
        catalog(args.inputfile)
    else:
        parser.error("Don't know what to do, an action (encrypt, decrypt or "+
                    "catalog) is mandatory")
        print args
