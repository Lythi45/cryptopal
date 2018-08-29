def xor(a,b):
    hex=b"0123456789abcdef"
    x_str=b""
    for i in range(len(a)):
        x_str+=bytes([hex[hex.find(a[i])^hex.find(b[i])]])
    return x_str

def hex2str(a):
    hex=b"0123456789abcdef"
    h_str=b""
    for i in range(0,len(a),2):
        h_str+=bytes([hex.find(a[i])*16+hex.find(a[i+1])])
    return h_str

def b2hex(a):
    hex=b"0123456789abcdef"
    return bytes([hex[a//16],hex[a&15]])

def str2hex(str):
    h_str=b""
    for c in str:
        h_str+=b2hex(c)
    return h_str


space_hex=b2hex(ord(' ')) #Leerzeichen ist am häufigsten

def stats(c_str):
    b_str=hex2str(c_str)
    stat={}
    for c in b_str:
        stat[c]=stat.get(c,0)+1
    max_c=max(stat, key=lambda key: stat[key])

    max_hex=b2hex(max_c)
    return len(stat),max_hex,stat[max_c]

string=b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
code=b"ICE"

h_string=str2hex(string)
h_code=str2hex((code*(len(string)//len(code)+1))[:len(string)])
code_str=xor(h_string,h_code)
print(code_str)

if code_str==b"0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f":
    print("OK")
