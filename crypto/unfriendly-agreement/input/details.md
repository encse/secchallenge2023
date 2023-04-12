Challenge Details
=================

Bob needs to implement a two-party two-message adaptor signature
scheme based on the MuSig protocol and Schnorr signatures.
You can read about all of these things on the Internets :)

The following are the details Alice and Bob agreed about the protocol:

- They use the Secp256k1 elliptic curve.
- They always use big endian byte order.
- They always use the SHA256 hashing algorithm.
- They always use UTF-8 encoding.
- They represent points on the elliptic curve as bytes by concatenating the
  byte representations of the x and y coordinates of the point.
- They always use the order (Alice's, Bob's) when sorting public keys.
- They chose to encode the multiset of public keys by hashing it.

In the `data.json` file you can find all the information that is known by Bob
at this point of the protocol. The following is a short explanation of what
each key-value pair in the file means.

- M1: Alice's message
- M2: Bob's message
- XA: Alice's permanent public key
- xB: Bob's permanent private key
- XB: Bob's permanent public key
- RA1: Alice's nonce public key for Alice's message
- rB1: Bob's nonce private key for Alice's message
- RB1: Bob's nonce public key for Alice's message
- RA2: Alice's nonce public key for Bob's message
- rB2: Bob's nonce private key for Bob's message
- RB2: Bob's nonce public key for Bob's message
- O: Alice's public offset
- SA1: Alice's offset signature for Alice's message
- SA2: Alice's offset signature for Bob's message
- sC1: Common signature for Alice's message

The flag is the common signature for Bob's message as an integer, wrapped in
in the CTF's flag format `cd23{}`.

Note: As you can see Bob does not know his signatures for the messages. He
obviously had them before, since Alice was able to use them during the later
stages of the protocol. Silly Bob, must have forgotten where he had written
them down. I guess you will need to calculate the signatures from scratch.
