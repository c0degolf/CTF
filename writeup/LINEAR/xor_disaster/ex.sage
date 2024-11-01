from disaster import *
from tqdm import tqdm

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

inp = GFvar([(1 << i) for i in range(256)][::-1])
sols = [246, 44, 115, 230, 101, 35, 204, 151, 20, 200, 112, 111, 231, 74, 41, 189, 95, 22, 222, 90, 58, 130, 0, 172, 1, 236, 89, 243, 80, 113, 242, 112]

res = []
for i in tqdm(range(32)):
    res.append(eval(f"xor{i}(inp)").bits)

A, B = [], []
for i in range(32):
    for j in range(8):
        a = [(res[i][j] >> k) & 1 for k in range(256)]
        A.append(a)
        B.append([(sols[i] >> j) & 1])

A = Matrix(GF(2), A)
B = Matrix(GF(2), B)

X = A.inverse() * B
X = sum([int(X[i][0]) << (255-i) for i in range(256)])

for i in range(32):
    assert eval(f"xor{i}(X)") == sols[i]

FLAG = "DH{" + hex(X)[2:] + "}"
raise ZeroDivisionError(FLAG)