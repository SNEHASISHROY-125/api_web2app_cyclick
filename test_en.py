# from cryptography.fernet import Fernet
# from fastapi import concurrency

key_ = b'OhR3XmFx14ArZLLCaOw9_ptnOjGbDYqNbY_W-kRNqu0='
msgg_ = b'gAAAAABk51tqZPldiKQ0EmAv_o4GbRen9BPgioxc8bFbmFTXQeIXuYtvzndovc2VnkZH27KJCRM7Zz-YjReAjq6jWVO9-fQPvvH7gP8kTf2xxBxtZJdWU4HA1uXkbzetpDGHMcxPdqas'
key = b'bHE4cl3Qmu-epB1XKjkYSw0ItVFMAVn9Fyiw-BRP_2Q='
encrypted_message = b'gAAAAABk51qXqEq-cmF4OlUhgrKtHt7DSJwU6T0_h0uvjcwtRBzaTQJCvDg4ubdvz-36kkkKUiCRunD729Y-KA8_1RzuoW2xlGd7amvuCPhYNKtDUiht9ZE='
'''
# Create a new Fernet cipher with the same key
decipher = Fernet(key_)

# Decrypt the encrypted message
decrypted_message = decipher.decrypt(msgg_)

# print("Decrypted Message:", decrypted_message.decode())

from hashing import encrypt ,decrypt , generate_key

decrypt(
    key_=key,
    msgg_body=b'gAAAAABk53JC0FSjev0PVRe3SvVrVwUGIMS4IXVTYdF8XLSEoFw8pw-tj5wFCTbiPxuHXCxKD9woz14_eG9Tm0D6CRaKx1ZegfL0wOTglaVGs1F-2snMcKosqmYTqvknRI-r6JhmDd8fIUq7QvjeuePCKo-G60AwH1gemfVMdfBdTE4T46ePdubNTnQMTHieyx6BC6DeXGgNSh9waxTKQs9HUHege1qj6RJejh7jQXqxSg31Q-PAwBdEhIT1S-KeAMmwTFk4ij_aAXVgA8CvNfqh1R_oXGr3w9pj1G4ET9YWBaWBIXg6GTtS4Uau-KJ40EiBYfvYS55t1tbxP5wWAFvX0OPY8JJgPWc8Ibw7s1cZYl06QSd95tlOhQTBLkJWL5RCfb-GR5gahdMZALlbH5ZciT2aVTZAxYw_pIUoDKDTBtPJO38df4comwRaHoQtYIqi60XW8pwSEg_u-BxPr4rub8n9fdep2G2ONegLNO8O6lR5eHYxXyR3SkZpa-GD629DDfx_IbCIOddKI0ltiHSMZ4sl4RKg7LHFeDUDftir2SOpKDMWq0B-kojIbCRzI21BLB911TM6du5ZImSyMXdxZAs51JfbcQYfZgMB_2HqGUvluQTTYNrjfBB1e_xSH3ahgJ5CFOIoEqW232ottnSfENaKkCfy-W_Jeesj1RglGZMUJm9vOX6KvVytaG9qptKxB_L8ioeDQsnkTPzMPdaEdEt4-YM3aw=='
)

# Token_error: decrypt
# try: ...
# except InvalidToken: ...

# def import_():
from syncDB import get_DB,put_DB,clear_DB,bucket,put_key,user_key
import hashing as hsh
import concurrent.futures
# with concurrent.futures.ThreadPoolExecutor() as executor: executor.submit(import_)
import threading
# print(msgg_)
# thread = threading.Thread(target=import_)
# thread.start()
# thread.join()


import concurrent.futures
# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit the get_DB function to the executor
    user_db = executor.submit(get_DB, bucket, user_key)
    get_db = executor.submit(get_DB,bucket,put_key)
    # Wait for the function to complete and get the result
    user = user_db.result()  # This will block until the function completes
    file_val= get_db.result()

# print('put started')

if file_val: print('Got:get_DB')
if user: print('User: recived!')

print('All are completed!',user ,file_val)

import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    get = executor.submit(get_DB,bucket,user_key)
    val = executor.submit(generate_key)
    # print(type(val))
    executor.submit(print,'val: started')
    executor.submit(clear_DB,key=put_key,schema=user_schema)
    val = val.result()
    print(val)

    get = get.result()
    print('getDB: ends', type(get))

print('all end')
'''

# Your string representation of bytes
string_representation = "b'ksNQ9J6XyUGXDTazGIPaOSEeqzj33mBXr0Pxf-OXp5U='"
def decode_to_bytes(payload:str) ->bytes:
    import ast
    # import concurrent.futures
    # Use ast.literal_eval to safely evaluate the string as bytes
    bytes_data = ast.literal_eval(payload.encode('utf-8').decode('unicode_escape'))
    return bytes_data
    # with concurrent.futures.ThreadPoolExecutor() as executor: executor.submit(sync)

# Now, bytes_data contains the actual bytes
# print(decode_to_bytes(string_representation))

# thread.join()
def add_user_data(user_id ,add_method ,msgg, file_val = None):
    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the get_DB function to the executor
        user_db = executor.submit(get_DB, bucket, user_key)
        get_db = executor.submit(get_DB,bucket,put_key)
        # Wait for the function to complete and get the result
        user = user_db.result()  # This will block until the function completes
        user_key_ = hsh.decode_to_bytes(user[user_id]['key'])
        print(user_key_)
        file_val= get_db.result()

# add_user_data(user_id='polly',add_method='msgg',msgg='hello')

# hsh.decrypt(key_=key_,msgg_body=b'gAAAAABk6Hv545fZ2BiGBq_4x7NdQAKcg5-FtkKjrjk_eI9J3lgMwObrzoXH5uqv4IhpKhnF1aiE_Vv4YjlRv7XUxexbPrfafg==')
# print(hsh.Hash().verify('password','$2b$12$aF86eKytAeItzDsoIxvQmOEeHAdkgWUoPbgtZuuiPTPrgEopl4DfW'))

email = "example124@gmail.com"

# Find the last occurrence of '@' and take the substring before it
# index = email.rfind("@")
# if index != -1:(user_name:= email[:index])
# else:
#     username = email  # If there's no '@' symbol, use the whole string

user_ = email.rindex('@')
# print(email[:user_])
# if 'rsnehasish15' in (U_data:=get_DB(key=user_key)).keys(): print('yes')
# print(U_data)

# get_DB(key=user_key)
# clear_DB(key=user_key)



def generate_unique_code(input_string):
    def strt():
        def imp_str(): 
            import string
            import random

        str_ = threading.Thread(target=imp_str)
        str_.start()
        str_.join()
    # threading.Thread(target=imp_str).start()
        # Define characters to use for generating the code (you can customize this)
        characters = string.ascii_letters + string.digits
        # Generate a random code
        random_code = ''.join(random.choice(characters) for _ in range(len(input_string)))
        return random_code 
    return strt()

user_email = "rsnehasish125@gmail.com"
# unique_code = generate_unique_code(input_string)
# print(user_id:=user_email[:user_email.rindex('@')])
# print(hsh.Hash().verify('PQCOIaQnTmdCpVvGFFoAtFY','$2b$12$vfGdp0pA9MmY052Mp7m.NeIEUcMB715PqM9WkveAuXBMje5zXoIIG'))
# get_DB(key=user_key)

# u = 'halo'
# a = 'halo'
# if a == u: print('match')