#! /usr/bin/python3
from cryptography.fernet import Fernet

def enc():
 #Key generation  and just run only for first time
 key = Fernet.generate_key()
 print("The encrypt key is:", key)

 # string the key in a file
 with open('/home/exampleuser/filekey.key', 'wb') as filekey:
  filekey.write(key)

 # Opening the key
 with open('/home/exampleuser/filekey.key', 'rb') as filekey:
  key = filekey.read()

 # using the generated key
 fernet = Fernet(key)

 # opening the original file to encrypt
 with open('/home/exampleuser/config.py', 'rb') as file:
  original = file.read()

 # encrypting the file
 encrypted = fernet.encrypt(original)

 # opening the file in write mode and
 # writing the encrypted data
 with open('/home/exampleuser/config.py', 'wb') as encrypted_file:
   encrypted_file.write(encrypted)

# Run this script only once for first time and comment\
# after that below function call
# Later script is called from main script publishCV.py
# Do not uncomment once file is encrypted.
#enc()
