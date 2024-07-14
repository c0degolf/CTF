from tqdm import tqdm
from chal import SmolPRNG
from pwn import *

class GFvar:
    def __init__(self, bits : list):
        while (bits[-1] == 0 and len(bits) != 1):
            bits.pop()
        self.bits = bits

    def __rshift__(self, shift : int) -> 'GFvar':
        bits = self.bits

        while (bits[-1] == 0 and len(bits) != 1):
            bits.pop()

        if shift >= len(bits):
            return GFvar([0])

        return GFvar(bits[shift:])

    def __lshift__(self, shift : int) -> 'GFvar':
        return GFvar([0] * shift + self.bits)

    def __xor__(self, other : 'GFvar | int') -> 'GFvar':
        bits = self.bits

        if isinstance(other, GFvar):
            other = other.bits
        else:
            other = [(other >> i) & 1 for i in range(int(other).bit_length())]

        sl, ol = len(bits), len(other)

        if sl == ol:
            new_v = [(bits[i] ^^ other[i]) for i in range(sl)]

        elif sl > ol:
            new_v = [(bits[i] ^^ other[i]) for i in range(ol)] + bits[ol:]

        else: # sl < ol
            new_v = [(bits[i] ^^ other[i]) for i in range(sl)] + other[sl:]

        return GFvar(new_v)

    def __and__(self, other : 'GFvar | int') -> 'GFvar':
        bits = self.bits

        if isinstance(other, GFvar):
            other = other.bits
        else:
            other = [(other >> i) & 1 for i in range(int(other).bit_length())]

        sl, ol = len(bits), len(other)

        new_v = []
        for i in range(min(sl, ol)):
            if other[i] == 0:
                new_v.append(0)
            else:
                new_v.append(bits[i])
        
        return GFvar(new_v)

    def __repr__(self) -> str:
        return f'{self.bits}'

counter, consts = 0, [0xa0e37a42, 0xa57f1a93, 0x83bb9b44]

state = [(1 << i) for i in range(512)]
state = [GFvar(state[i:i+32][::-1]) for i in range(0, 512, 32)]

def con(const, state):
    return GFvar([(state.bits[-1] if i == '1' else 0) for i in bin(const)[2:]])

def step():
    global state, counter
    for i in range(16):
        i1, i2 = [(i + j + 1) % 16 for j in range(2)]
        state[i] = (
            (state[i] >> 1) ^ con(consts[0], state[i])
            ^ (state[i1] >> 1) ^ con(consts[1], state[i1])
            ^ (state[i2] >> 1) ^ con(consts[2], state[i2])
        )

    counter = 0

def gen() -> int:
    global state, counter
    if counter == 16:
        step()
    
    y = GFvar(state[counter].bits[:])
    y ^= (y >> 7)
    y ^= (y << 11) & 0xb5547000
    y ^= (y << 13) & 0xf5230000
    y ^= (y >> 17)
    
    counter += 1
    return (y & 0xffff).bits 

for _ in tqdm(range(1000)): step()

M = []
for i in tqdm(range(50)):
    coeffs = gen()

    assert len(coeffs) == 16
    for coeff in coeffs:
        c = [0 for _ in range(512)]
        for i in range(512):
            if ((coeff >> (511-i)) & 1) == 1:
                c[i] = 1
        M.append(c)

context.log_level = 'error'
p = process(["python3", "chal.py"])
# p = remote("host3.dreamhack.games", 17722)

p.recvuntil(b":\n")

B = []
for i in tqdm(range(50)):
    val = int(p.recvline().strip().decode())
    for j in range(16):
        B.append((val >> (15-j)) & 1)

M = Matrix(GF(2), M)
B = vector(GF(2), B)

bin_to_int = lambda n : sum([(int(n[i]) << i) for i in range(len(n))])

seed = list(M.solve_right(B))
seed = [bin_to_int(seed[::-1][i:i+32]).to_bytes(4, 'little') for i in range(0, 512, 32)]

prng = SmolPRNG(b''.join(seed))
for _ in range(50):
    prng.gen()

for i in tqdm(range(16)):
    p.sendlineafter(b'> ', str(prng.gen()).encode())

FLAG = p.recvlineafter(b": ")[:-1].decode()
raise ZeroDivisionError(FLAG)