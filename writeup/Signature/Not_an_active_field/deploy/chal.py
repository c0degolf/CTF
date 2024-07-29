from Crypto.Cipher import AES
import hashlib
from machine import TreeParityMachine
from secret import flag
import numpy as np
from Crypto.Util.Padding import pad


def encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, 16)).hex()


k, l, n = 7, 10, 10
Alice = TreeParityMachine(k, n, l, "hebian")
Bob = TreeParityMachine(k, n, l, "hebian")

inputs = []
alice_taus = []
bob_taus = []

for _ in range(1000):
    x = np.random.randint(-25, 26, Alice.n * Alice.k)
    t1 = Alice.forward(x)
    t2 = Bob.forward(x)
    inputs.append(list(x))
    alice_taus.append(t1)
    bob_taus.append(t2)
    if t1 == t2:
        Alice.backward(Bob.tau)
        Bob.backward(Alice.tau)
        
        
assert np.array_equal(Bob.W, Alice.W)
assert Bob.W.shape == (k, n)

sha256 = hashlib.sha256()
sha256.update(Alice.W.tobytes())
key = sha256.digest()
ct = encrypt(key, flag)

with open("output.txt", "w") as f:
    f.write(f"ct = {ct}\n")
    f.write(f"inputs = {inputs}\n")
    f.write(f"alice_taus = {alice_taus}\n")
    f.write(f"bob_taus = {bob_taus}\n")