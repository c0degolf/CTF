import hashlib
from tqdm import tqdm
from ecdsa.numbertheory import square_root_mod_prime
from pwn import *

io = remote("blinders.2024.ctfcompetition.com", int(1337))
context.log_level = 'error'

io.recvline() # == proof-of-work: disabled ==

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
K = GF(p)
a = K(0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc)
b = K(0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b)
E = EllipticCurve(K, (a, b))
G = E(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
E.set_order(0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551 * 0x1)

def H(id):
    hash = hashlib.sha256(f'id={id}'.encode()).digest()
    x = int.from_bytes(hash, 'big')

    while True:
        y2 = (x**3 + a*x + b) % p
        if jacobi_symbol(y2, p) == 1: break
        x += 1

    y = square_root_mod_prime(*map(int, [y2, p]))
    return E(x, y)

eid_1 = sum([H(i) for i in range(0, 256, 2)])
eid_2 = sum([H(i) for i in range(1, 256, 2)])

def sol():
    io.sendline(f"handle {eid_1.xy()[0]} {eid_1.xy()[1]}".encode())

    eids1 = eval(io.recvline())
    deid1 = eval(io.recvline())

    eids1 = [E(*eids1[i]) for i in range(255)]
    deid1 = E(*deid1)

    io.sendline(f"handle {eid_2.xy()[0]} {eid_2.xy()[1]}".encode())

    eids2 = eval(io.recvline())
    deid2 = eval(io.recvline())

    eids2 = [E(*eids2[i]) for i in range(255)]
    deid2 = E(*deid2)

    for i in range(256):
        S = [*range(256)]
        S.remove(i)

        if i%2:
            idx = [S.index(j) for j in range(0, 256, 2)]
            if sum([eids1[j] for j in idx]) == deid1:
                return S

        else:
            idx = [S.index(j) for j in range(1, 256, 2)]
            if sum([eids2[j] for j in idx]) == deid2:
                return S

for _ in tqdm(range(16)):
    S = sol()
    io.sendline(f"submit {hashlib.sha256(','.join(map(str,S)).encode()).hexdigest()}".encode())
    io.recvuntil(b"OK!\n")

raise ZeroDivisionError(io.recvline(keepends=False).decode())