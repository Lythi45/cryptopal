from Crypto.Cipher import AES

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



f=open("10.txt",'r')
code=""
for lin in f:
    code+=lin.strip()
hex_code=b64_hex(code)

key="YELLOW SUBMARINE"

decipher = AES.new(key, AES.MODE_ECB)
hex_plain=cbc_decode(decipher,'0'*32,hex_code)
print(hex2str(hex_plain))

hex_code2=cbc_encode(decipher,'0'*32,hex_plain)
if (hex_code==hex_code2):
    print ("Reencoden klappt")
