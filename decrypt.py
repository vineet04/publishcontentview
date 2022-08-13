#! /usr/bin/python3

from cryptography.fernet import Fernet

def dec():
# opening the key
 with open('/home/exampleuser/filekey.key', 'rb') as filekey:
      key = filekey.read()
 fernet = Fernet(key)
 with open('/home/exampleuser/config.py', 'rb') as enc_file:
      encrypted = enc_file.read()
# print(encrypted)

 decrypted = fernet.decrypt(encrypted)
# result=(decrypted.decode())
# final=(result.strip())
 check="ok"
#print(check)
#print(final)
 with open('/home/satellite/scripts/config.py', 'wb') as dec_file:
    dec_file.write(decrypted)

 return(dec_file)

#dec()
