from Crypto.Util.number import getPrime, long_to_bytes
from pwn import *
from tqdm import tqdm

pbits = 1024

primes = []
flags = []
mods = []

base = 1
for small_p in Primes():
    base *= small_p 
    if int(base).bit_length() >= pbits - 20:
        break

k = 2^pbits // base 
p = k*base + 1

while len(primes) != 77:
    if p.is_prime(): 
        primes.append(p)
    p -= base

p = process(["python3", "prob.py"])

NtoH = lambda n : hex(int(n))[2:].encode()

for i in tqdm(range(77)):
    prime = primes[i]

    p.sendlineafter(b"> ", NtoH(prime))
    p.sendlineafter(b"> ", NtoH(prime-1))

    # y = g^flag mod prime
    # log g y = flag mod mul_order(g)
    F = GF(prime)

    g = F(int(p.recvlineafter(b"= "), 16))
    y = F(int(p.recvlineafter(b"= "), 16))
    order = g.multiplicative_order()

    flag = discrete_log(y, g, order)
    flags.append(flag)
    mods.append(order)

    assert pow(g, flag, p) == y
    assert pow(g, order, p) == 1

FLAG = long_to_bytes(crt(flags, mods))
REAL_FLAG = FLAG[:FLAG.find(b"}")+1].decode()

print(REAL_FLAG)