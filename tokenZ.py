'''
JWT token
'''

import datetime
import getpass
import os

# Get the value of the environment variable 'smtp_key'
smtp_key = os.environ.get('smtp_key')

# Check if the environment variable exists
if smtp_key is None:
    raise ValueError("!smtp_key is not set in the environment")

# Now you can use 'smtp_key' in your script
# print('api:',smtp_key)
print(datetime.datetime.utcnow())


import secrets

# Generate a random 256-bit (32-byte) secret key
secret_key = secrets.token_hex(32)

# Print the secret key (make sure to store it securely)
# print('secrete_key:',secret_key)



# Use getpass to securely input a password
# input_ = getpass.getpass("Enter your password: ")
# print(input_)
import hashing as Hsh
# hshed_pwd = Hsh.Hash().bcrypt(input_)

# print(hshed_pwd)

# Verify the password

import bson

# Define a dictionary to represent your data
def dump(data_to_write):
    # Serialize the data to BSON
    bson_data = bson.encode(data_to_write)

    # Write the BSON data to a file
    with open("data.bson", "wb") as file:
        file.write(bson_data)

def retreive():
    # Read the BSON data from the file
    with open("data.bson", "rb") as file:
        read_bson_data = file.read()

    # Deserialize the BSON data to a Python dictionary
    retrieved_data = bson.decode(read_bson_data)
    return retrieved_data

# Print the retrieved data
# print(data:=retreive())
'''
dump({
    'user_id' : {
        'password': f'{None}',
        'email': f'{None}'
    }
})
'''

from cryptography.fernet import Fernet

# Generate a random symmetric key
# key = Fernet.generate_key()
# key = b'bHE4cl3Qmu-epB1XKjkYSw0ItVFMAVn9Fyiw-BRP_2Q='
# print('key:',key)

def encrypt(key:bytes,msgg_body:str):
    # Create a Fernet cipher using the key
    cipher = Fernet(key)
    # Message to encrypt
    message = msgg_body.encode()

    # Encrypt the message
    encrypted_message = cipher.encrypt(message)

    print("Encrypted Message:", encrypted_message)

def decrypt(key_, msgg_body):
    # Create a new Fernet cipher with the same key
    decipher = Fernet(key_)

    # Decrypt the encrypted message
    decrypted_message = decipher.decrypt(msgg_body)

    print("Decrypted Message:", decrypted_message.decode())

