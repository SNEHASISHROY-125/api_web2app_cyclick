'''
Communication with AWS S3 Bucket (Background)

Three Table: Admin , User , Message-Respoonse
JSON-is used for now , in FUTURE vertions will shift to BSON
'''
# Default Schema for messages annd response
chat_schema = {
    'user_id': {
        'message': {},
        'response': {}
    }
}
# User :
user_schema = {
    'user_id' : {
        'name': None,
        'password': f'{None}',
        'email': f'{None}',
        'key' : 'key'
    }
}
# Admin :
admin_schema = {
    'admin_id': {
        'password': f'{None}',
        'email': f'{None}'
    }
}

# Default SETTING's:
bucket = "cyclic-ruby-grasshopper-boot-us-west-1"
get_bucket , put_bucket = bucket , bucket

# pip install boto3
import boto3
# s3 = boto3.client('s3')
import datetime
import json
import threading
import concurrent.futures
import hashing as hsh


def import_():
    from hashing import generate_key,Hash,encrypt,decrypt,decode_to_bytes
    # import concurrent.futures
    # with concurrent.futures.ThreadPoolExecutor() as executor: executor.submit(import_)
# import threading
# thread = threading.Thread(target=import_)
# thread.start()
# thread.join()

# admin credential: "some_files/demo_credentials_file.json"
# func to add/set up admin credentials:
# SETIING's:
admin_key = "some_files/demo_credentials_file.json"
def set_admin_credentials(admin_id, password=None, email=None):
    password = ... # hashed password
    email = ...
    # add dict that contains the credentials:
    admin_DB =get_DB(key=admin_key)
    # check if user admin exists:
    if not admin_id in admin_DB.keys():
        admin_DB[admin_id] = (admin_schema.copy()).pop('admin_id')
        print(admin_DB)
        boto3.client('s3').put_object(
                    Body=json.dumps(admin_DB),
                    Bucket= bucket,
                    Key= admin_key
                )
        print('S Done!')
    else: print('ADMIN already exists!','\n',admin_DB.keys())

# DELETE: Admin:
def del_admin_credentials(admin_id,password=None,bucket=bucket,key=admin_key,) -> dict:
    # get admin_DB:
    admin_DB =get_DB(key=key)
    # check if admin_id exists:
    if admin_id in admin_DB.keys():
        # verify using Hash(password) ....
        # delete admin_id
        admin_DB.pop(admin_id)
        if admin_DB ==  {}: admin_DB = []
        response=put_DB(key=key,body=admin_DB)
        if response == 'Done': print(f'Deleted USER with id: {admin_id}')
    else: print(f"id: {admin_id} doesn't exist")

# GET-schemma | for key:
get_key = "some_files/demo_file.json"
def get_schema(key=None) -> dict:
    if key:
        try:
            if key == admin_key: schema_ = admin_schema
            elif key == get_key: schema_ = chat_schema
            elif key == user_key: schema_ = user_schema
            return schema_
        except NameError:
            print(f"Didn't find any schema for: {key}")
            return {}

# GET: DB | Using -> key,bucket:
def get_DB(bucket=get_bucket,key=get_key) ->dict:
    '''
    key -> file name.
    '''
    print('Wait! Fetching Data...')
    my_file = boto3.client('s3').get_object(
        Bucket=bucket,
        Key=key
    )
    # converts from json to readable type:
    response = json.loads(my_file['Body'].read())
    print('recived response from key:', response)
    if isinstance(response , dict):
        return (response)
    else:
        schema_ = get_schema(key=key)
        print(f'Not dict type!Setting to\n{schema_}')
        clear_DB(key=key)
        return None

# TESTING file: "some_files/demo_file.json"
# to clear the file:  clear_DB()
def clear_DB(bucket=bucket,key=admin_key,schema=None) -> dict:
    '''Clears the key-file | value set to default Schema'''
    # user_concent = input(f'Are you sure you want to clear {key} ? (y/n): ')
    # if user_concent == 'y':
    #     verify_credentials = input('Enter ADMIN credentials: ')
    #     # verify credentials using hash
        # if verify_credentials == 'admin':  # Change this to your admin password
    if not schema: schema = get_schema(key=key)
    if schema:
        boto3.client('s3').put_object(
            Body = json.dumps(schema),
            Bucket=bucket,
            Key=key
        )
        print(f'Done! File Set to {schema}')
        return  True
    else: ...

# SETIING's:
put_key = "some_files/demo_file.json"
## STORE: something
def put_DB(bucket=put_bucket,key=None,body=None) -> None:
    ''' Dumps dict '''
    if body is None or key is None:
        return 'No body was given'
    else:
        # pass dict to dump:
        if isinstance(body, dict):
            boto3.client('s3').put_object(
                Body=json.dumps(body),
                Bucket= bucket,
                Key= key
            )
            return 'Done'
        else:
            print(f'body in {key} is not a dict')
            clear_DB(key=key)
# SETTING's:
user_key = "some_files/demo_user_file.json"
# ADD: USER
def add_user(bucket=bucket ,key=user_key ,user_id=None,name_=None,password=None,email=None):
    '''Adds user | user_id, password, email'''
    def sync(user_id,key):
        chat_DB = get_DB(key=key)
        # also add to chat_DB:
        print('async',chat_DB)
        chat_DB[user_id] = (chat_schema.copy()).pop('user_id')
        if 'user_id' in chat_DB.keys(): chat_DB.pop('user_id')
        put_DB(key=key,body=chat_DB)
    if user_id is None:
        print('No user_id was given')
        return 'No user_id was given'
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            user_ = executor.submit(get_DB,bucket,key)
            key_=executor.submit(hsh.generate_key)
            private_key = key_.result()
            user_DB = user_.result()
        if isinstance(user_DB, dict):
            if not user_id in user_DB.keys():
                # add to user_DB:
                user_DB[user_id] = (user_schema.copy()).pop('user_id')
                user_DB[user_id]['name'] = name_
                user_DB[user_id]['password'] = hsh.Hash().bcrypt(password)
                user_DB[user_id]['email'] = email
                user_DB[user_id]['key'] = f'{private_key}' # GENERATED-private-key 
                if 'user_id' in user_DB.keys(): user_DB.pop('user_id')
                put_DB(key=key,body=user_DB)
                threading.Thread(target=sync,args=(user_id,put_key)).start()
                return 'Done'
            else: print(f'User with id: {user_id} already exists!')
        else: clear_DB(key=key,schema=user_schema)

# DELETE: USER
def del_user(user_id,password=None,bucket=bucket,key=user_key):
    del_admin_credentials(admin_id=user_id,password=password,bucket=bucket,key=key)
    DB = get_DB(key=get_key)
    if user_id in DB:
        DB.pop(user_id)
        put_DB(key=get_key,body=DB)
        return True
    else: return False #f'No User Named {user_id}'

# ADD: USER DATA
def add_user_data(user_id ,add_method ,msgg, file_val = None):
    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the get_DB function to the executor
        user_db = executor.submit(get_DB, bucket, user_key)
        get_db = executor.submit(get_DB,bucket,put_key)
        # Wait for the function to complete and get the result
        user = user_db.result()  # This will block until the function completes
        user_key_ = hsh.decode_to_bytes(user[user_id]['key'])
        file_val= get_db.result()
     # file_val = get_DB(key=get_key)
    # Call bassed on mode 
    add_msgg_ = None
    if add_method == 'add_response': 
        add_msgg_ = add_response(key=user_key_,response_body=msgg)
    elif add_method == 'add_msgg': 
        add_msgg_ = add_msgg(key=user_key_,msgg_body=msgg)
    if not add_msgg_: return False
    # Ncrypt: 

    if isinstance(file_val, dict):
        if user_id in file_val.keys():
            # add messg to main file & dump
            file_val[f'{user_id}'][f'{add_msgg_[2]}'][add_msgg_[0]] = add_msgg_[1]
            # pass to put_DB method:
            # body = json.dumps(file_val)
            put_DB(body=file_val,key=put_key)
        else: print('user dosent exitst' ,file_val)

def add_msgg(key:bytes,msgg_body:str) ->str: 
    '''Returns key : value as tuple'''
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    msgg_val_tuple = (
        f"{timestamp}" , f"{hsh.encrypt(key=key,msgg_body=msgg_body)}"
    )
    return msgg_val_tuple + ('message',)

def add_response(key:bytes,response_body:str) ->str:
    '''Returns key : value as tuple'''
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    msgg_val_tuple = (
        f"{timestamp}" , f"{hsh.encrypt(key=key,msgg_body=response_body)}"
    )
    return msgg_val_tuple + ('response',)

def get_user(user_id):
    print(user_id)
    if user_id == '*': 
        k = get_DB(key=user_key).keys()
        return zip(range(len(k)),k)
    else: 
        if user_id in (U_data:=get_DB(key=user_key)).keys():return U_data[user_id]
        else: return f'No User Named {user_id}'

# print(get_user(user_id='zill'))
# add_user(user_id='roy',email='rsnehasish125@gmail.com',password='r125@W2a')
# del_user(user_id='roy')
# add_user_data(user_id='roy',add_method=add_response ,msgg='🍺🍩😅🍨🎈')
# del_admin_credentials(admin_id='poly97')
# set_admin_credentials(admin_id='poly97' , password='admin')
# clear_DB(key=put_key)

# print(get_DB(key=user_key))