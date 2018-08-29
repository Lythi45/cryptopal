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

space_hex=b2hex(ord(' ')) #Leerzeichen ist am häufigsten

def stats(c_str):
    b_str=hex2str(c_str)
    stat={}
    for c in b_str:
        stat[c]=stat.get(c,0)+1
    max_c=max(stat, key=lambda key: stat[key])

    max_hex=b2hex(max_c)
    return len(stat),max_hex,stat[max_c]

f=open("4.txt",'rb')
ln=0
for lin in f:
    line=lin.strip()
    ln+=1
    #print(line)
    #print(hex2str(line.strip()))
    lst,max_hex,nmh=stats(line)
    key=xor(max_hex,space_hex)
    #print(key)
    if nmh>4:
        print(ln,nmh)
        print(line)
        print(hex2str(xor(line,key*(len(line)//2))))
