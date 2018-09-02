from Crypto.Cipher import AES
import random

def random_key():
    return  "".join(map(chr,[random.randint(32,127) for i in range(16)]))
global_key=random_key()

def padding(text):
    pad_l=16-len(text)%16
    return text+bytes([pad_l])*pad_l

def unpadding(text):
    return text[:-text[-1]]

def ebc_encode(key,plain):
    decipher = AES.new(key, AES.MODE_ECB)
    return decipher.encrypt(padding(plain))

def ebc_decode(key,code):
    decipher = AES.new(key, AES.MODE_ECB)
    return unpadding(decipher.decrypt(code))

def sani(text):
    return text.replace('&','').replace('=','')

def profile_for(email):
    return 'email='+sani(email)+'&id=10&role=user'

def parse_profile(profile):
    return {j[0]:j[1] for j in [i.split('=') for i in profile.split('&')]}

def encode_profile(profile_str):
    return ebc_encode(global_key,profile_str.encode('ascii'))

def oracle(email):
    return encode_profile(profile_for(email))

def login_admin(code):
    if parse_profile(ebc_decode(global_key,code).decode('ascii'))['role']=='admin':
        print ('Access as Admin granted')
    else:
        print('Access is denied!')

evil_email='xxxxxxxxxxadmin'+chr(11)*11 #fake-padding in second block
evil_code=oracle(evil_email)
admin_block=evil_code[16:32]

email='x'*14 #email=xxxxxxxxxxxxxx&id=10&role= #32 Chars
code=oracle(email)
access_code=code[:32]+admin_block

login_admin(access_code)
