import getpass
import os
import sys
import pam
from cryptography.hazmat.primitives import hashes,hmac
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class User():

    def __init__(self,):
        self._username = os.getlogin()
        self._filename = 'root/etc/' + self._username
        temporarySession = True
        getOut = False
        nAttempts = 0
        while(not(getOut)):
            self._password = getpass.getpass()
            if(pam.authenticate(self._username, self._password)):
                getOut = True
                temporarySession = False
            else: 
                print("Wrong authentication data!")
                nAttempts = nAttempts + 1    
            if(nAttempts == 3):
                getOut = True
                print("Too many attempts: authentication failed!")
        if(temporarySession):
            print("We could not recognize your authentication data!")
            print("This session will last only while the file system is not closed!\n")
            print("Please enter contact information (email or phone number)")
            info = input("-->")
            self._contact = info
        else:
            try:
                file = open(self._filename, 'rb')
                encrypted_contact = file.read()
                nonce = encrypted_contact[:16]
                salt = encrypted_contact[16:32]
                contact = encrypted_contact[32:]
                backend = default_backend()
                kdf = PBKDF2HMAC(
                    algorithm = hashes.SHA256(),
                    length = 32,
                    salt = salt,
                    iterations = 100000,
                    backend = backend
                )   
                key = kdf.derive(self._password.encode())
                algorithm = algorithms.ChaCha20(key,nonce)
                cipher = Cipher(algorithm,mode=None,backend = default_backend())
                decryptor = cipher.decryptor()
                dt = decryptor.update(contact)         
                self._contact = dt.decode()
                file.close()
            except FileNotFoundError:
                print("Please enter contact information (email or phone number)")
                info = input("-->")
                self._contact = info
                nonce = os.urandom(16)
                backend = default_backend()
                salt = os.urandom(16)
                kdf = PBKDF2HMAC(
                    algorithm = hashes.SHA256(),
                    length = 32,
                    salt = salt,
                    iterations = 100000,
                    backend = backend
                )   
                key = kdf.derive(self._password.encode())
                algorithm = algorithms.ChaCha20(key,nonce)
                cipher = Cipher(algorithm,mode=None,backend = default_backend())
                encryptor = cipher.encryptor()
                ct = encryptor.update(self._contact.encode())
                message_to_write = nonce + salt + ct
                file = open(self._filename, 'wb')
                file.write(message_to_write)
                file.close()