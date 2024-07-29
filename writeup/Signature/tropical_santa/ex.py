from tqdm import tqdm
from pwn import *
from tropical import *
from hashlib import sha256
from string import ascii_letters, digits
from itertools import product
import re

# context.log_level = True
# p = process(["python3", "task.py"])
p = remote("host1.dreamhack.games", 18035)

tmp = p.recvlineafter(b"SHA-256( XXXX + ").split()
back = tmp[0]
hsh = bytes.fromhex(tmp[-1].decode())

CHARSET = string.ascii_letters + string.digits
for i in product(CHARSET, repeat=4):
    candidate = "".join(i).encode() + back
    if hashlib.sha256(candidate).digest() == hsh:
        p.sendlineafter(b" > ", "".join(i).encode())
        break

p.recvline() # welcome

r, d = 127,150
user_msg = b"Amelia Watson"
H = Polynomial.hash_message(user_msg,r,d)
N = Polynomial.random(r=2*r,d=2*d)

for _ in tqdm(range(10)):
    p.recvline() # stage
    
    M = Polynomial([Elem(int(v)) for v in p.recvlineafter(b"Polynomial(")[:-4].decode().split()])
    
    p.recvline()
    p.recvline()
    p.sendlineafter(b" > ", user_msg.hex().encode())
    A = H*M
    B = H*N
    T = A*B
    assert A*B == H*H*M*N
    _A = (T/(B*H))*H
    _B = (T/(A*H))*H

    p.sendlineafter(b"1 > ", " ".join(map(str, H.coefs)).encode())
    p.sendlineafter(b"2 > ", " ".join(map(str, _A.coefs)).encode())
    p.sendlineafter(b"3 > ", " ".join(map(str, _B.coefs)).encode())
    p.sendlineafter(b"4 > ", " ".join(map(str, N.coefs)).encode())

raise ZeroDivisionError(re.search('DH{.*}', p.recvall().decode()).group())