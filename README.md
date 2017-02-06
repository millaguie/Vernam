# Vernam

Here is a Vernam cipher implementation in python. My goal with this project is
achive my degree in CS ;) but also create a optimized way to use Vernam cipher
in the real world(TM).

This implementation rely on a huge file filled with real random data shared
with another person. For example Alice and Bob (original me).

Alice will be our creator, the person who created the huge file and Bob will be
the consumer. It's important to identify this two roles, because the use of the
key file (that huge random generated file) will be different for each user.

Creator will use the file from the beggining to the end, meanwhile consumer will
do it in reverse, from the end to the beggining. This is the way create a
bidirectional commmuncation with only a file. As key data availability (last
consumer minus last creator position used) drops under a certain thresold,
software will alert you to meet your fella and interchange a new key file, and
to prevent you to reuse key file. As soon the key is reused, software will
alert you, so if this happend it's on your own. If this happend it's pretty
difficult to break the whole message but, an interceptor can start to work.
