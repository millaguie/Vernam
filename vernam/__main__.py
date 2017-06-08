# -*- coding: utf-8 -*-
"""
This is the main file of vernam encryption.
Please refer to readme.md for general information about this software,
refer to license.md for license information
"""
import argparse
import configuration
import vernam
import keymanagement



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
    actionGr.add_argument('--printable', required=False, action='store_true',
                          help="Write to outputfile a printable version of the"+
                          " key, ready to be used by humans. Warning! this could"+
                          " be huge.")

    # encrypt or decryption can operate in one mode but only one
    modeGr = parser.add_mutually_exclusive_group()
    modeGr.add_argument('--lz4', action='store_true', default=False,
                        help="Use lz4 compression mode")
    modeGr.add_argument('--raw', action='store_true', default=False,
                        help="Use raw mode (default option)")
    modeGr.add_argument('--human', action='store_true', default=False,
                        help="Use mode for humans")

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
    parser.add_argument("--l2r", action='store_true', default=False,
                        help="When catalogging a key, select read mode right "+
                        "to left, by default will use left to right")
    args = parser.parse_args()


    # Read configuration file
    configFromFile = configuration.readConfig(args.config)
    if args.lz4 is True:
        mode = "lz4"
    elif args.raw is True:
        mode = "raw"
    elif args.human is True:
        mode = "human"
    else:
        mode = "raw"

    # merge configuration from command line and config file
    config = configuration.parseConfig(configFromFile, args, mode)
    print("input file: {}, output file: {}, config file: {}, ".format(
        args.inputfile, args.outputfile, args.config)
          + "key file: {}, operation mode: {}".format(config["keyfile"],
                                                      config["workmode"]))
    print(config["workmode"])
    if args.encrypt is True:
        vernam.encrypt(args.inputfile, config["keyfile"], args.outputfile,
                       force=args.force, mode=config["workmode"])
    elif args.decrypt is True:
        vernam.decrypt(args.inputfile, config["keyfile"], args.outputfile,
                       force=args.force, mode=config["workmode"])
    elif args.catalog is True:
        keymanagement.catalog(args.inputfile, args.l2r, force=args.force)
    elif args.printable is True:
        keymanagement.printable2file(args.inputfile, args.outputfile, force=args.force)
    else:
        parser.error("Don't know what to do, an action (encrypt, decrypt or "+
                     "catalog) is mandatory")
        print (args)
