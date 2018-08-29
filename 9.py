str=input("String?")
block_len=16

padding=block_len-1-(len(str)+block_len-1)%block_len

str=str+chr(padding)*padding
print(str)
