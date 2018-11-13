Deterministic GPG key generation
=============================

Deterministic GPG key creation.  

Using your own entropy to generate cryptographic keys allows you to:
- be more secure, as you can generate your entropy from a variety of sources (dice, HRNG)
- be more resilient, as you can store your entropy in a desirable format (mnemonic, cryptosteel)

The [Glacier Protocol](https://glacierprotocol.org/) offers a clear guideline on how to generate Bitcoin keys from your own entropy.
If you like their methodology, and want to use it for other cryptographic tools like GPG keys, this repo is for you!

Requirements
------------

- [GPG](http://gnupg.org)
- [MonkeySphere](http://web.monkeysphere.info/)
- [PyCryptodome](https://github.com/Legrandin/pycryptodome) which is a fork of PyCrypto

How to use
----------

    python3 entropy_to_gpg.py

Then follow instructions. The script will allow you to:
- generate entropy from dice and device (you will be prompted before this action is taken)
- feed entropy to PRNG
- use PRNG to derive RSA key
- convert RSA key to GPG format
- import RSA key into GPG keyring (you will be prompted before this action is taken)

Issues
------

1. PyCryptodome's RSA key generation requires a RNG [here](https://github.com/Legrandin/pycryptodome/blob/master/lib/Crypto/PublicKey/RSA.py#L444) to generate > 100000 bytes. This repo uses [SHAKE](https://docs.python.org/3/library/hashlib.html#shake-variable-length-digests) as a deterministic drop-in replacement using the hash of the mnemonic as a seed. Is this correct?

   Alternatives may be [AES-CTR](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html) or [pbkdf2_hmac](https://docs.python.org/2/library/hashlib.html#key-derivation). The repository from which this code was forked used an uncommon library: [HMAC_DRBG](https://github.com/fpgaminer/python-hmac-drbg/tree/aa09924419266a6ad478022ae3da32eab4587c8f).

2. Is PyCryptodome's [RSA key generation](https://github.com/Legrandin/pycryptodome/blob/master/lib/Crypto/PublicKey/RSA.py#L390) safe? Are more trusted libraries available? 
4. Is any tool available to convert an elliptic curve point to a GPG key? At the moment, pem2openpgp only converts RSA pem keys
