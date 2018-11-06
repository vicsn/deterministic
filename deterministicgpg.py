#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  Copyright 2014 Arttu Kasvio <arttu@ubuntu>
#  
# This is free and unencumbered software released into the public domain.
# See LICENSE for more info and refer to <http://unlicense.org>

# Requirements: pycrypto, monkeysphere, gpg

import sys
import os
import drbg
import getpass
import hashlib
import subprocess
from Crypto.PublicKey import RSA


def create_gpg_key(user_id, seed):
  
  rand = drbg.HMAC_DRBG(seed)

  key = RSA.generate(4096, rand.read)

  # Since we're auto-generating the key default the creation time to UNIX time 0
  os.environ['PEM2OPENPGP_TIMESTAMP'] = '0'

  #pem2openpgp "Foo Bar <fbar@linux.net>" < priv.pem | gpg --import
  pem2openpgp = subprocess.Popen(['pem2openpgp', user_id], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  gpg_id = pem2openpgp.communicate(key.exportKey(pkcs=1))[0]
  return gpg_id

def import_gpg_key(gpg_id):
  gpg_import = subprocess.Popen(['gpg', '--import'], stdin=subprocess.PIPE)
  gpg_import.communicate(gpg_id)

if __name__ == '__main__':
  import sys
  name = ""
  email = ""
  
  # get name/email for GPG id
  name = raw_input('Name: ')
  email= raw_input('Email: ')

  user_id = '%s <%s>' % (name, email)

  # Example electrum seeds for test:
  #   action draw bit shove single however shore language visit wonderful swell pale
  #   motion shut tool sadness focus scratch wash match torture tightly situation jump
  seed ="action draw bit shove single however shore language visit wonderful swell pale motion shut tool sadness focus scratch wash match torture tightly situation jump"
  if(raw_input("do you want to give a custom seed? (y/n)") == "y"):
      seed = raw_input()
        
  gpg_id = create_gpg_key(user_id, seed)
  if(raw_input("do you actually want to import the generated key into your gpg keyring? (y/n)") == "y"):
    import_gpg_key(gpg_id)
