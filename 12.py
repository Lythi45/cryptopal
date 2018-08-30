from Crypto.Cipher import AES
import random

append_b64="Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

def b64_hex(str):
    p_str="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    hex="0123456789abcdef"
    h_str=""
    for i in range(0,len(str),4):
        n=0
        for j in range(4):
            n=n*64+p_str.find(str[i+j])
        hs=""
        for j in range(6):
            hs=hex[n&15]+hs
            n=n>>4
        h_str+=hs
    return h_str


def humming_d(a,b):
    hex="0123456789abcdef"
    bits=[0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4]
    humm_dist=0
    for i in range(len(a)):
        humm_dist+=bits[hex.find(a[i])^hex.find(b[i])]
    return humm_dist

def xor(a,b):
    hex="0123456789abcdef"
    x_str=""
    for i in range(len(a)):
        x_str+=hex[hex.find(a[i])^hex.find(b[i])]
    return x_str

def hex2str(a):
    hex="0123456789abcdef"
    h_str=""
    for i in range(0,len(a),2):
        h_str+=chr(hex.find(a[i])*16+hex.find(a[i+1]))
    return h_str

def hex2byte(a):
    hex="0123456789abcdef"
    h_str=b""
    for i in range(0,len(a),2):
        h_str+=bytes([hex.find(a[i])*16+hex.find(a[i+1])])
    return h_str

def b2hex(a):
    hex="0123456789abcdef"
    return hex[a//16]+hex[a&15]

def bytes2hex(bytes):
    hex=""
    for b in bytes:
        hex+=b2hex(b)
    return hex

def str2hex(str):
    h_str=""
    for c in str:
        h_str+=b2hex(ord(c))
    return h_str

def cbc_encode(decipher,ini_vector,cipher):
    plain=""
    vector=ini_vector
    for i in range(0,len(cipher),32):
        xor_block=xor(vector,cipher[i:i+32])
        vector=bytes2hex(decipher.encrypt(hex2byte(xor_block)))
        plain+=vector
    return plain

def cbc_decode(decipher,ini_vector,plain):
    cipher=""
    vector=ini_vector
    for i in range(0,len(plain),32):
        block=plain[i:i+32]
        enc_block=bytes2hex(decipher.decrypt(hex2byte(block)))
        cipher+=xor(vector,enc_block)
        vector=block
    return cipher

def ebc_encode(decipher,plain):
    return bytes2hex(decipher.encrypt(hex2byte(plain)))

def random_key():
    return  "".join(map(chr,[random.randint(32,127) for i in range(16)]))
global_key=random_key()

def random_stuff():
    return  "".join(map(chr,[random.randint(0,255) for i in range(random.randint(5,10))]))

def encryption_oracle(text):
    key=global_key
    decipher = AES.new(key, AES.MODE_ECB)
    plain=text+hex2str(b64_hex(append_b64))
    padd_len=15-(len(plain)+15)%16
    hex_plain=str2hex(plain+chr(padd_len)*padd_len)


    code=ebc_encode(decipher,hex_plain)
    return hex2str(code)

oracle_code=encryption_oracle("A"*15)
odic={}
for i in range(256):
    code=encryption_oracle("A"*15+chr(i))
    odic[code[:16]]=i
first_char=chr(odic[oracle_code[:16]])

oracle_code=encryption_oracle("A"*14)
odic={}
for i in range(256):
    code=encryption_oracle("A"*14+first_char+chr(i))
    odic[code[:16]]=i
second_char=chr(odic[oracle_code[:16]])
print(first_char,second_char)

le=len(encryption_oracle(""))
lle=le
l=0
while le==lle:
    l+=1
    lle=len(encryption_oracle("A"*l))
code_len=le-l+1
print("Code-Length:",code_len)

plain_text=""
for i in range(code_len):
    print(i)
    oracle_code=encryption_oracle("A"*((15-i)%16))
    odic={}
    block_num=i//16
    for c in range(256):
        code=encryption_oracle("A"*((15-i)%16)+plain_text+chr(c))
        odic[code[block_num*16:(block_num+1)*16]]=c
    plain_text+=chr(odic[oracle_code[block_num*16:(block_num+1)*16]])
print(plain_text)
