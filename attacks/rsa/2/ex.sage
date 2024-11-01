from Crypto.Util.number import *

# ==================================
m = b"Common modulus attack"
m = bytes_to_long(m)

N = getPrime(1024) * getPrime(1024)

e = 3

c = pow(m, e, N)
# ==================================

for k in range(0x10001):
    try:
        m = ZZ(c+k*N).nth_root(e)
        print(long_to_bytes(int(m)))
    except:
        continue