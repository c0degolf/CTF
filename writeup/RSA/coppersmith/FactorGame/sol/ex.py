from pwn import *
from sage.all import *
from lll_cvp import small_roots

con = process(["python3", "FactorGame.py"])
lim = 264

def mine(rnd):
    global p, q
    
    if rnd == lim:
        if p * q % (1 << (rnd+1)) == N % (1 << (rnd+1)):
            _p, _q = p, q
            if not ((_p, _q) in candidates or (_q, _p) in candidates):
                candidates.append((_p, _q))
        return

    for s1 in range(2):
        for s2 in range(2):
            if p_arr[rnd] != 2 and p_arr[rnd] != s1:
                continue
            if q_arr[rnd] != 2 and q_arr[rnd] != s2:
                continue

            if (p + (s1 << rnd)) * (q + (s2 << rnd)) % (1 << (rnd + 1)) == N % (1 << (rnd + 1)):
                p += (s1 << rnd)
                q += (s2 << rnd)
                mine(rnd + 1)
                p -= (s1 << rnd)
                q -= (s2 << rnd)

for _ in range(10):
    p_redacted = int(con.recvlineafter(b'p : ')[2:], 16) | 1
    p_mask = int(con.recvlineafter(b'p_mask : ')[2:], 16) | 1
    q_redacted = int(con.recvlineafter(b'q : ')[2:], 16) | 1
    q_mask = int(con.recvlineafter(b'q_mask : ')[2:], 16) | 1
    N = int(con.recvlineafter(b'N : ')[2:], 16)

    p_arr = []
    q_arr = []

    for i in range(512):
        if (p_mask&1 == 1):
            p_arr.append(p_redacted&1)
        else:
            p_arr.append(2)

        p_redacted >>= 1
        p_mask >>= 1

        if (q_mask&1 == 1):
            q_arr.append(q_redacted&1)
        else:
            q_arr.append(2)

        q_redacted >>= 1
        q_mask >>= 1

    p, q = 0, 0
    candidates = []

    mine(0)
    
    candi = []
    # for pp, qq in candidates:
    # for i in range(263, -1, -1):
    #     if p_arr[i] != 2 and p_arr[i-1] == 2:
    #         if q_arr[i] != 2 and q_arr[i-1] == 2:
    #             p_high, q_high = p_arr[i], q_arr[i]
    #             lim = i
    #             break

    # for p, q in candidates:
    #     p = p + (p_high << lim)
    #     q = q + (q_high << lim)
    #     if p*q % (1 << (lim + 1)) == N % (1 << (lim + 1)):
    #         candidates.append((p,q))

    print(len(candidates))
    for p_low, q_low in candidates:
        print(p_low.bit_length())
        P = PolynomialRing(Zmod(N), names=('x')); (x, ) = P._first_ngens(1)
        f = (p_low + 2**lim * x).monic()
        rs = small_roots(f, X=2**(512-lim), beta=0.499, epsilon=0.015)
        if len(rs) == 0:
            print("no root")
            continue
        else:
            print("yay!")
        p = p_low + 2**lim * int(rs[0])
        q = N // p
        assert p * q == N
        
        con.sendlineafter(b": ", hex(p)[2:].encode())
        con.sendlineafter(b": ", hex(q)[2:].encode())
        print(con.recvline())
        break