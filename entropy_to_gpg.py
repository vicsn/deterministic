#!/usr/bin/env python3

import deterministicgpg as dgpg
import mnemonic 
import glacierscript_minimal as glacier
import binascii


if __name__ == "__main__":
    # initialize variables
    n = int(input("how many keys do you want to generate? "))
    dice = int(input("how many dicerolls do you want to do? "))
    amount_of_bytes = int(input("how many bytes (two hexadecimal chars) entropy do you want? "))
    amount_of_strings = int(input("how many times do you want to query dev/random to get your entropy? "))

    # do checklist
    glacier.safety_checklist()
    
    # generate entropy
    glacier.entropy(amount_of_strings, amount_of_bytes/amount_of_strings) 
    
    # mix entropy
    keys = glacier.deposit_interactive(n, dice, amount_of_bytes) 
    for k in keys:
        # generate mnemonic
        data = binascii.unhexlify(keys[0])
        m = mnemonic.Mnemonic('english')
        mnemonic_str = m.to_mnemonic(data)
        print("mnemonic key: ", mnemonic_str)
      
        # generate GPG key
        name = input('Name: ')
        email= input('Email: ')
        user_id = '%s <%s>' % (name, email)
        gpg_id = dgpg.create_gpg_key(user_id, mnemonic_str)
        print("key generated") 

        # import GPG key
        if(input("are you sure you want to import the new key into gpg? (y/n) ") == "y"):
            dgpg.import_gpg_key(gpg_id)
    
