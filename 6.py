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

def b2hex(a):
    hex="0123456789abcdef"
    return hex[a//16]+hex[a&15]

def str2hex(str):
    h_str=""
    for c in str:
        h_str+=b2hex(ord(c))
    return h_str


s1="this is a test"
s2="wokka wokka!!!"
print(humming_d(str2hex(s1),str2hex(s2)))

f=open("6.txt",'r')
code=""
for lin in f:
    code+=lin.strip()

hex_code=b64_hex(code)
print(hex_code)

x=75
for key_len in range(2,41):
    hu=humming_d(hex_code[x:x+key_len*2],hex_code[x+key_len*2:x+key_len*4])/key_len
    print(key_len,hu)

key_len=29

space_hex=b2hex(ord(' ')) #Leerzeichen ist am häufigsten
b_str=hex2str(hex_code)
keys={}
for pos in range(key_len):
    p_str=""
    for i in range(pos,len(b_str),key_len):
        p_str+=b_str[i]
    #print(len(p_str))
    stat={}
    for c in p_str:
        stat[c]=stat.get(c,0)+1
    #print(stat)
    max_c=max(stat, key=lambda key: stat[key])
    #print(stat[max_c])
    max_hex=b2hex(ord(max_c))

    key=xor(max_hex,space_hex)
    keys[pos]=key
    print("{2} Key ist {1}, in Hex: {0}".format(key,hex2str(key),max_hex))

klar_hex=""
for i in range(0,len(hex_code)-2,2):
    pos=(i//2)%key_len
    klar_hex+=xor(keys[pos],hex_code[i:i+2])
print(klar_hex)
print(hex2str(klar_hex))
