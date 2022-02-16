from cryptography.fernet import Fernet
"""
Author 		: 	Sridhar
Created On 	: 	2020-Sep-28 5:58 PM
Usage 		: 	encrypt and decrypt for url parameters and strings
Eg 			: 
 				encrypted = Cryptography.encrypt("my text")
				encrypted (output) : gAAAAABfcdgFt4T9tR3ixH00UVqJGQvMyu-WmIpWjxp3EVNZCq1M_uvlTZKD7X2PJXRDafJFfCZhpyVU0CaZstcenVm5s0oemQ==
				decrypted = Cryptography.decrypt(encrypted)
				decrypted (output) : my text
"""
class Cryptography:
	def generate_key():
	    """
	    Generates a key and save it into a file
	    """
	    key = Fernet.generate_key()
	    with open("secret.key", "wb") as key_file:
	        key_file.write(key)

	def load_key():
	    """
	    Loads the key named `secret.key` from the current directory.
	    """
	    return open("secret.key", "rb").read()


	def encrypt(value):
	    """
	    Encrypts a message
	    """
	    key = Cryptography.load_key()
	    encoded_value = repr(value).encode('utf-8')
	    f = Fernet(key)
	    encrypted_value = f.encrypt(encoded_value)

	    return encrypted_value.decode()


	def decrypt(encrypted_value):
	    """
	    Decrypts an encrypted message
	    """
	    key = Cryptography.load_key()
	    f = Fernet(key)
	    decrypted_value = f.decrypt(bytes(encrypted_value + "==",'utf-8'))

	    return decrypted_value.decode()