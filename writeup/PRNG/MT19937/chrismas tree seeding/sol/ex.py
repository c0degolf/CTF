import random
from seed import *
from pwn import *

getstate = lambda x : random.Random(x).getstate()

assert 2**40000 <= s_int1 < 2**80000
assert 2**20000 <= s_int2 < 2**40000
assert 2**2000  <= s_int3 < 2**20000
assert 0        <= s_int4 < 2**2000
assert             s_int5 < 0

assert s_str == s_int1.to_bytes(10000, "big")[-len(s_str):].decode()

context.log_level = 'error'
p = remote("host3.dreamhack.games", 18023)

p.sendlineafter(b": ", str(s_int1).encode())
p.sendlineafter(b": ", str(s_int2).encode())
p.sendlineafter(b": ", str(s_int3).encode())
p.sendlineafter(b": ", str(s_int4).encode())
p.sendlineafter(b": ", str(s_int5).encode())
p.sendlineafter(b": ", s_str.encode())
p.sendlineafter(b": ", s_bytes.hex().encode())
print(p.recvline()[:-1].decode())