from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

# pwd_cxt.verify(request.password, user.password)
class Hash():
    def bcrypt(self ,password: str) ->str:
        # hashed_pwd = pwd_cxt.hash(password)
        return pwd_cxt.hash(password)
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_cxt.verify(plain_password, hashed_password)

# print(Hash().bcrypt('admin'))


from cryptography.fernet import Fernet

# Generate a random symmetric key
# key = Fernet.generate_key()
# key = b'bHE4cl3Qmu-epB1XKjkYSw0ItVFMAVn9Fyiw-BRP_2Q='
# print('key:',key)
def generate_unique_code(input_string: str) ->str:
    import random, string
    # Define characters to use for generating the code (you can customize this)
    characters = string.ascii_letters + string.digits
    # Generate a random code
    random_code = ''.join(random.choice(characters) for _ in range(len(input_string)))
    return random_code 

def generate_key()-> bytes:
    return Fernet.generate_key()

def decode_to_bytes(payload:str) ->bytes:
    # import concurrent.futures
    import ast
    # Use ast.literal_eval to safely evaluate the string as bytes
    bytes_data = ast.literal_eval(payload.encode('utf-8').decode('unicode_escape'))
    return bytes_data
    # with concurrent.futures.ThreadPoolExecutor() as executor: executor.submit(sync)

def encrypt(key:bytes,msgg_body:str) ->bytes:
    # Create a Fernet cipher using the key
    cipher = Fernet(key)
    # Message to encrypt
    message = msgg_body.encode()
    # Encrypt the message
    encrypted_message = cipher.encrypt(message)

    print("Encrypted Message:", encrypted_message)
    return encrypted_message

def decrypt(key_:bytes, msgg_body:bytes) ->str:
    # Create a new Fernet cipher with key_
    decipher = Fernet(key_)
    # Decrypt the encrypted message
    decrypted_message = decipher.decrypt(msgg_body)

    print("Decrypted Message:", decrypted_message.decode())
    return decrypted_message.decode()
