# Vernam
[![Build Status](https://travis-ci.org/millaguie/Vernam.svg?branch=master)](https://travis-ci.org/millaguie/Vernam)
[![Documentation Status](https://readthedocs.org/projects/vernam/badge/?version=latest)](http://vernam.readthedocs.io/en/latest/?badge=latest)

# Vernam cipher for the real world

Here is a Vernam cipher implementation in python. My goal with this project is
achive my degree in CS ;) but also create a optimized way to use Vernam cipher
to exchange message in the real world(TM).

This implementation rely on a huge file filled with real random data shared
with another person. For example Alice and Bob (original me).

Alice will be our creator, the person who created the huge file and Bob will be
the consumer. It's important to identify this two roles, because the use of the
key file (that huge random generated file) will be different for each user.

Creator will use the file from the beggining to the end, meanwhile consumer will
do it in reverse, from the end to the beggining. This is the way to create a
bidirectional commmuncation with only a file. As key data availability (last
consumer minus last creator position used) drops under a certain thresold, user
must meet your fella and interchange a new key file. Users may be on alert to
prevent reuse key file. If this happend it's pretty difficult to break the whole
message but, an interceptor, can start to work.

## Getting started

Software is developed in Python 2.7, and works like any other command line tool,
Written in Python.

### Prerequisites

To start using this software you need some software prerequisites:

* Python 2.7 installed (system wide or virtual environment)
* Install all required modules listed in requirements.txt (pip install -r
   Requirements.txt, will work)

The key step to use this encryption method is to choose a good randomness
source, this examples uses /dev/urandom but you can use any other source of
your choose.

### Installing

Just follow this steps:

```
if [[ $(python --version 2>&1) == *2\.7* ]]; then   
  git clone https://github.com/millaguie/Vernam.git
  cd Vernam
  sudo pip install -r requirements.txt
else
  echo "Not running python 2.7"
fi
```

And everything must work

## Firsts steps with Vernam cipher for the real world

The first step is to get a random fille key:

```
dd if=/dev/urandom of=keyfile count=1024 bs=1024
```

Second, catalog the key file

```
alice@securesystem1:~/Vernam$ python -m vernam --catalog -i keyfile
input file: keyfile, output file: None, config file: config.yaml, key file: defaultrawfile.rnd, operation mode: lz4
Generating hash of key, this might take some time
```
This first run will generate a configuration file for the software (if don't exists) and a catalog file for the key.

Now you can exchanege key and catalog file with your fella. Your fella will need
edit yaml file to change l2r attribute to true, he or she will be key's
consumer.

```
bob@securesystem2:~/Vernam$ diff keyfile.yaml keyfile.yaml.alice
3c3
< l2r: true
---
> l2r: false

```

As Alice you can create a message file and send it to Bob.
```
alice@securesystem1:~/Vernam$ echo Meet me at the gates ASAP > secretmessage.txt
alice@securesystem1:~/Vernam$ python -m vernam -e -k keyfile -i secretmessage.txt -o sendbob
input file: secretmessage.txt, output file: sendbob, config file: config.yaml, key file: keyfile, operation mode: lz4
32 of 1048576 bytes will be in use after this action
```
Send output file to bob via an insecure system.

And bob will be able to read message using the shared key:

```
bob@securesystem2:~/Vernam$ python -m vernam -d -k keyfile -i sendbob -o secretmessage.txt
input file: sendbob, output file: secretmessage.txt, config file: config.yaml, key file: keyfile, operation mode: lz4
Output file will be overwritten as requested.
32 of 1048576 bytes will be in use after this action
bob@securesystem2:~/Vernam$ cat secretmessage.txt
Meet me at the gates ASAP
```

You can get more information from --help switch

```
$ python -m vernam --help
usage: __main__.py [-h] [-e | -d | --catalog | --printable]
                   [--lz4 | --base32 | --raw | --human] -i INPUTFILE
                   [-o OUTPUTFILE] [-c CONFIG] [-k KEYFILE] [-f] [--l2r]

Vernam cipher implementation

optional arguments:
  -h, --help            show this help message and exit
  -e, --encrypt         Start in encryption mode
  -d, --decrypt         Start in decryption mode
  --catalog             Catalog a new keyfile
  --printable           Write to outputfile a printable version of the key,
                        ready to be used by humans. Warning! this could be
                        huge.
  --lz4                 Use lz4 compression mode
  --base32              Use base32 mode
  --raw                 Use raw mode (default option)
  --human               Use mode for humans
  -i INPUTFILE, --inputfile INPUTFILE
                        File to encrypt or decrypt, when using in catalog mode
                        keyfile to catalog
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        File to store output, stdout by default
  -c CONFIG, --config CONFIG
                        Path to configuration file
  -k KEYFILE, --keyfile KEYFILE
                        Path to a file containing the random data used as key
                        for the cipher
  -f, --force           Force to overwrite output file
  --l2r                 When catalogging a key, select read mode right to
                        left, by default will use left to right

```
## Author

* **Fco. Javier Picado Ladrón de Guevara** - [millaguie](https://github.com/millaguie)

## License
This project is licensed under BSD 3-clause "New" or "Revised" License - see the
[LICENSE](LICENSE) file for details
