from cryptography.fernet import Fernet
# from fastapi import concurrency

key_ = b'OhR3XmFx14ArZLLCaOw9_ptnOjGbDYqNbY_W-kRNqu0='
msgg_ = b'gAAAAABk51tqZPldiKQ0EmAv_o4GbRen9BPgioxc8bFbmFTXQeIXuYtvzndovc2VnkZH27KJCRM7Zz-YjReAjq6jWVO9-fQPvvH7gP8kTf2xxBxtZJdWU4HA1uXkbzetpDGHMcxPdqas'
key = b'bHE4cl3Qmu-epB1XKjkYSw0ItVFMAVn9Fyiw-BRP_2Q='
encrypted_message = b'gAAAAABk51qXqEq-cmF4OlUhgrKtHt7DSJwU6T0_h0uvjcwtRBzaTQJCvDg4ubdvz-36kkkKUiCRunD729Y-KA8_1RzuoW2xlGd7amvuCPhYNKtDUiht9ZE='

# Create a new Fernet cipher with the same key
decipher = Fernet(key_)

# Decrypt the encrypted message
decrypted_message = decipher.decrypt(msgg_)

# print("Decrypted Message:", decrypted_message.decode())

from hashing import encrypt ,decrypt , generate_key
'''
decrypt(
    key_=key,
    msgg_body=b'gAAAAABk53JC0FSjev0PVRe3SvVrVwUGIMS4IXVTYdF8XLSEoFw8pw-tj5wFCTbiPxuHXCxKD9woz14_eG9Tm0D6CRaKx1ZegfL0wOTglaVGs1F-2snMcKosqmYTqvknRI-r6JhmDd8fIUq7QvjeuePCKo-G60AwH1gemfVMdfBdTE4T46ePdubNTnQMTHieyx6BC6DeXGgNSh9waxTKQs9HUHege1qj6RJejh7jQXqxSg31Q-PAwBdEhIT1S-KeAMmwTFk4ij_aAXVgA8CvNfqh1R_oXGr3w9pj1G4ET9YWBaWBIXg6GTtS4Uau-KJ40EiBYfvYS55t1tbxP5wWAFvX0OPY8JJgPWc8Ibw7s1cZYl06QSd95tlOhQTBLkJWL5RCfb-GR5gahdMZALlbH5ZciT2aVTZAxYw_pIUoDKDTBtPJO38df4comwRaHoQtYIqi60XW8pwSEg_u-BxPr4rub8n9fdep2G2ONegLNO8O6lR5eHYxXyR3SkZpa-GD629DDfx_IbCIOddKI0ltiHSMZ4sl4RKg7LHFeDUDftir2SOpKDMWq0B-kojIbCRzI21BLB911TM6du5ZImSyMXdxZAs51JfbcQYfZgMB_2HqGUvluQTTYNrjfBB1e_xSH3ahgJ5CFOIoEqW232ottnSfENaKkCfy-W_Jeesj1RglGZMUJm9vOX6KvVytaG9qptKxB_L8ioeDQsnkTPzMPdaEdEt4-YM3aw=='
)
'''
# Token_error: decrypt
# try: ...
# except InvalidToken: ...

from syncDB import get_DB ,put_key ,user_key , bucket ,clear_DB , user_schema

'''
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
'''
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