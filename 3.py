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

c_str="1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

space_hex=b2hex(ord(' ')) #Leerzeichen ist am häufigsten
b_str=hex2str(c_str)
stat={}
for c in b_str:
    stat[c]=stat.get(c,0)+1
max_c=max(stat, key=lambda key: stat[key])

max_hex=b2hex(ord(max_c))

# häufigstes Zeichen aus dem Code-String wird mit ' ' verXORt für den Key, damit
# beim verXORen des Codes wieder das Leerzeichen erscheint
key=xor(max_hex,space_hex)

print("Key ist {1}, in Hex: {0}".format(key,hex2str(key)))
print(hex2str(xor(c_str,key*(len(c_str)//2))))
