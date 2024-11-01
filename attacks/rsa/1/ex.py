from Crypto.Util.number import *

# ==================================
m = b"Common modulus attack"
m = bytes_to_long(m)

N = getPrime(1024) * getPrime(1024)

e1 = getPrime(17)
e2 = getPrime(17)

c1 = pow(m, e1, N)
c2 = pow(m, e2, N)
# ==================================

def EEA(a, b):
    if a == 0:
        return 0, 1
    else:
        x, y = EEA(b%a, a)
        return y-(b//a)*x, x

u, v = EEA(e1, e2)

assert GCD(e1, e2) == 1

pt = pow(c1, u, N) * pow(c2, v, N) % N
pt = long_to_bytes(pt)

assert pt == b"Common modulus attack"