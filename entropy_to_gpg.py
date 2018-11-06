import deterministicgpg as dgpg
import mnemonic 
import glacierscript_minimal as glacier
import binascii
from Crypto import Random


if __name__ == "__main__":
    n = input("how many keys do you want to generate? ")
    dice = input("how many dicerolls do you want to do? ")
    amount_of_bytes = input("how many bytes (two hexadecimal chars) entropy do you want? ")
    amount_of_strings = input("how many times do you want to query dev/random to get your entropy? ")

    glacier.safety_checklist()
    glacier.entropy(amount_of_strings, amount_of_bytes/amount_of_strings) 
    keys = glacier.deposit_interactive(n, dice, amount_of_bytes) 
    for k in keys:
        data = binascii.unhexlify(keys[0])
        m = mnemonic.Mnemonic('english')
        mnemonic_str = m.to_mnemonic(data)
        print("mnemonic key: ", mnemonic_str)
      
        name = raw_input('Name: ')
        email= raw_input('Email: ')
        user_id = '%s <%s>' % (name, email)
        rng = raw_input("using the pbkdf2_hmac as PRNG takes minutes. If you just want to test, you might want to use /dev/urandom\n" +
                        "- (0) use /dev/urandom\n" +
                        "- (1) use pbkdf2_hmac\n" +
                        "Please indicate which source you want to use (0/1): ")
        while(True):
            if rng == "0":
                gpg_id = dgpg.create_gpg_key(user_id, mnemonic_str, Random.new())
                break
            elif rng == "1":
                gpg_id = dgpg.create_gpg_key(user_id, mnemonic_str)
                break
            rng = raw_input("please pass a 0 or 1 and try again: ")

        print("key generated") 
        if(raw_input("are you sure you want to import the new key into gpg? (y/n) ") == "y"):
            dgpg.import_gpg_key(gpg_id)
    
