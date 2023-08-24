from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

# pwd_cxt.verify(request.password, user.password)
class Hash():
    def bcrypt(self ,password: str):
        # hashed_pwd = pwd_cxt.hash(password)
        return pwd_cxt.hash(password)
    
    def verify(self, plain_password, hashed_password):
        return pwd_cxt.verify(plain_password, hashed_password)

# print(Hash().bcrypt('admin'))


from cryptography.fernet import Fernet

# Generate a random symmetric key
# key = Fernet.generate_key()
# key = b'bHE4cl3Qmu-epB1XKjkYSw0ItVFMAVn9Fyiw-BRP_2Q='
# print('key:',key)

def generate_key()-> bytes:
    return Fernet.generate_key()

def encrypt(key:bytes,msgg_body:str):
    # Create a Fernet cipher using the key
    cipher = Fernet(key)
    # Message to encrypt
    message = msgg_body.encode()

    # Encrypt the message
    encrypted_message = cipher.encrypt(message)

    print("Encrypted Message:", encrypted_message)

def decrypt(key_:bytes, msgg_body:bytes):
    # Create a new Fernet cipher with the same key
    decipher = Fernet(key_)

    # Decrypt the encrypted message
    decrypted_message = decipher.decrypt(msgg_body)

    print("Decrypted Message:", decrypted_message.decode())
