from sage.all import *
from disaster import *
from tqdm import tqdm

class GFbits:
    def __init__(self, bits : list):
        while (bits[0] == F(0) and len(bits) != 1):
            bits.pop(0)
        self.bits = bits

    def __rshift__(self, shift : int) -> 'GFbits':
        if shift >= len(self.bits):
            return GFbits([F(0)])
        return GFbits(self.bits[:-shift])

    def __lshift__(self, shift : int) -> 'GFbits':
        return GFbits(self.bits + [F(0)] * shift)

    def __xor__(self, other : 'GFbits | int') -> 'GFbits':
        # in GF(2), xor and addition are the same.
        bits = self.bits

        if isinstance(other, int):
            other = [F(int(b)) for b in bin(other)[2:]]
        else:
            other = other.bits

        sl, ol = (len(bits), len(other))

        if sl == ol:
            pass
        elif sl > ol:
            other = [F(0)] * (sl-ol) + other
        else:
            bits = [F(0)] * (ol-sl) + bits

        new_v = [(bits[i] + other[i]) for i in range(max(sl, ol))]
        return GFbits(new_v)

    def __and__(self, other : int) -> 'GFbits':
        if other == BITMASK:
            return GFbits(self.bits[-256:])
        else: # other == 0xff
            return GFbits(self.bits[-8:])

    def __repr__(self) -> str:
        return f'{self.bits}'

def sol():
    eqs = ["xor0(v)", "xor1(v)", "xor2(v)", "xor3(v)", "xor4(v)", "xor5(v)", "xor6(v)", "xor7(v)", "xor8(v)", "xor9(v)", "xor10(v)", "xor11(v)", "xor12(v)", "xor13(v)", "xor14(v)", "xor15(v)", "xor16(v)", "xor17(v)", "xor18(v)", "xor19(v)", "xor20(v)", "xor21(v)", "xor22(v)", "xor23(v)", "xor24(v)", "xor25(v)", "xor26(v)", "xor27(v)", "xor28(v)", "xor29(v)", "xor30(v)", "xor31(v)"]

    for i in tqdm(range(32)):
        eqs[i] = eval(eqs[i])

    res = [246, 44, 115, 230, 101, 35, 204, 151, 20, 200, 112, 111, 231, 74, 41, 189, 95, 22, 222, 90, 58, 130, 0, 172, 1, 236, 89, 243, 80, 113, 242, 112]
    
    B = []
    for i in range(32):
        B += [[F(int(i))] for i in bin(res[i])[2:].zfill(8)]

    A = []

    for i in range(32):
        for j in range(8):
            try:
                eq = str(eqs[i][j]).split(" + ")
                eq = [int(e[1:]) for e in eq]
            except:
                # eq = ... + 1
                eq = str(eqs[i][j]).split(" + ")[:-1]
                eq = [int(e[1:]) for e in eq]

                B[i*8 + j][0] += F(1)
                
            coeff = [0] * 256
            for e in eq:
                coeff[e] = 1

            A.append(coeff)

    assert len(A) == 256 and all([len(i)==256 for i in A])
    assert len(B) == 256

    A = Matrix(F, A)
    B = Matrix(F, B)

    # Ax = B ( 256x256 * 256x1 = 256x1 )
    # x = B * A^-1
    x = A.inverse()*B

    x = [str(x[i, 0]) for i in range(256)]
    x = "".join(x)

    assert len(x) == 256

    inp = int(x, 2)

    # boooooooom
    for i in range(32):
        assert eval(f"xor{i}(inp)") == res[i]

    return inp

F = GF(2)['x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64, x65, x66, x67, x68, x69, x70, x71, x72, x73, x74, x75, x76, x77, x78, x79, x80, x81, x82, x83, x84, x85, x86, x87, x88, x89, x90, x91, x92, x93, x94, x95, x96, x97, x98, x99, x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111, x112, x113, x114, x115, x116, x117, x118, x119, x120, x121, x122, x123, x124, x125, x126, x127, x128, x129, x130, x131, x132, x133, x134, x135, x136, x137, x138, x139, x140, x141, x142, x143, x144, x145, x146, x147, x148, x149, x150, x151, x152, x153, x154, x155, x156, x157, x158, x159, x160, x161, x162, x163, x164, x165, x166, x167, x168, x169, x170, x171, x172, x173, x174, x175, x176, x177, x178, x179, x180, x181, x182, x183, x184, x185, x186, x187, x188, x189, x190, x191, x192, x193, x194, x195, x196, x197, x198, x199, x200, x201, x202, x203, x204, x205, x206, x207, x208, x209, x210, x211, x212, x213, x214, x215, x216, x217, x218, x219, x220, x221, x222, x223, x224, x225, x226, x227, x228, x229, x230, x231, x232, x233, x234, x235, x236, x237, x238, x239, x240, x241, x242, x243, x244, x245, x246, x247, x248, x249, x250, x251, x252, x253, x254, x255']
(x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64, x65, x66, x67, x68, x69, x70, x71, x72, x73, x74, x75, x76, x77, x78, x79, x80, x81, x82, x83, x84, x85, x86, x87, x88, x89, x90, x91, x92, x93, x94, x95, x96, x97, x98, x99, x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111, x112, x113, x114, x115, x116, x117, x118, x119, x120, x121, x122, x123, x124, x125, x126, x127, x128, x129, x130, x131, x132, x133, x134, x135, x136, x137, x138, x139, x140, x141, x142, x143, x144, x145, x146, x147, x148, x149, x150, x151, x152, x153, x154, x155, x156, x157, x158, x159, x160, x161, x162, x163, x164, x165, x166, x167, x168, x169, x170, x171, x172, x173, x174, x175, x176, x177, x178, x179, x180, x181, x182, x183, x184, x185, x186, x187, x188, x189, x190, x191, x192, x193, x194, x195, x196, x197, x198, x199, x200, x201, x202, x203, x204, x205, x206, x207, x208, x209, x210, x211, x212, x213, x214, x215, x216, x217, x218, x219, x220, x221, x222, x223, x224, x225, x226, x227, x228, x229, x230, x231, x232, x233, x234, x235, x236, x237, x238, x239, x240, x241, x242, x243, x244, x245, x246, x247, x248, x249, x250, x251, x252, x253, x254, x255) = F._first_ngens(256)
x = [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64, x65, x66, x67, x68, x69, x70, x71, x72, x73, x74, x75, x76, x77, x78, x79, x80, x81, x82, x83, x84, x85, x86, x87, x88, x89, x90, x91, x92, x93, x94, x95, x96, x97, x98, x99, x100, x101, x102, x103, x104, x105, x106, x107, x108, x109, x110, x111, x112, x113, x114, x115, x116, x117, x118, x119, x120, x121, x122, x123, x124, x125, x126, x127, x128, x129, x130, x131, x132, x133, x134, x135, x136, x137, x138, x139, x140, x141, x142, x143, x144, x145, x146, x147, x148, x149, x150, x151, x152, x153, x154, x155, x156, x157, x158, x159, x160, x161, x162, x163, x164, x165, x166, x167, x168, x169, x170, x171, x172, x173, x174, x175, x176, x177, x178, x179, x180, x181, x182, x183, x184, x185, x186, x187, x188, x189, x190, x191, x192, x193, x194, x195, x196, x197, x198, x199, x200, x201, x202, x203, x204, x205, x206, x207, x208, x209, x210, x211, x212, x213, x214, x215, x216, x217, x218, x219, x220, x221, x222, x223, x224, x225, x226, x227, x228, x229, x230, x231, x232, x233, x234, x235, x236, x237, x238, x239, x240, x241, x242, x243, x244, x245, x246, x247, x248, x249, x250, x251, x252, x253, x254, x255]

v = GFbits(x)

SOLUTION = hex(sol())[2:]
assert len(SOLUTION) == 64

print(f"DH{{{SOLUTION}}}")