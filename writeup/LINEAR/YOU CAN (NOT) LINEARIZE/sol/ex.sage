from pwn import *

P.<x00, x01, x02, x03, x10, x11, x12, x13, x20, x21, x22, x23, x30, x31, x32, x33> = PolynomialRing(Zmod(251))

f00 = lambda a : x00^2*a[0][0] + x00*x10*a[0][1] + x00*x20*a[0][2] + x00*x30*a[0][3] + x00*x10*a[1][0] + x10^2*a[1][1] + x10*x20*a[1][2] + x10*x30*a[1][3] + x00*x20*a[2][0] + x10*x20*a[2][1] + x20^2*a[2][2] + x20*x30*a[2][3] + x00*x30*a[3][0] + x10*x30*a[3][1] + x20*x30*a[3][2] + x30^2*a[3][3]
f11 = lambda a : x01^2*a[0][0] + x01*x11*a[0][1] + x01*x21*a[0][2] + x01*x31*a[0][3] + x01*x11*a[1][0] + x11^2*a[1][1] + x11*x21*a[1][2] + x11*x31*a[1][3] + x01*x21*a[2][0] + x11*x21*a[2][1] + x21^2*a[2][2] + x21*x31*a[2][3] + x01*x31*a[3][0] + x11*x31*a[3][1] + x21*x31*a[3][2] + x31^2*a[3][3]
f22 = lambda a : x02^2*a[0][0] + x02*x12*a[0][1] + x02*x22*a[0][2] + x02*x32*a[0][3] + x02*x12*a[1][0] + x12^2*a[1][1] + x12*x22*a[1][2] + x12*x32*a[1][3] + x02*x22*a[2][0] + x12*x22*a[2][1] + x22^2*a[2][2] + x22*x32*a[2][3] + x02*x32*a[3][0] + x12*x32*a[3][1] + x22*x32*a[3][2] + x32^2*a[3][3]
f33 = lambda a : x03^2*a[0][0] + x03*x13*a[0][1] + x03*x23*a[0][2] + x03*x33*a[0][3] + x03*x13*a[1][0] + x13^2*a[1][1] + x13*x23*a[1][2] + x13*x33*a[1][3] + x03*x23*a[2][0] + x13*x23*a[2][1] + x23^2*a[2][2] + x23*x33*a[2][3] + x03*x33*a[3][0] + x13*x33*a[3][1] + x23*x33*a[3][2] + x33^2*a[3][3]

context.log_level = 'error'
# io = process(["python3", "chal.py"])
io = remote("host3.dreamhack.games", int(23061))

As, Bs = [], []
for _ in range(4):
    A, B = [], []
    for i in range(4):
        a, b = io.recvline()[1:-2].split(b"] [")
        a = list(map(int, a.split()))
        b = list(map(int, b.split()))
        A.append(a)
        B.append(b)
    As.append(A)
    Bs.append(B)
    io.recvline()

eq00, eq11, eq22, eq33 = [], [], [], []
for i in range(4):
    eq00.append( f00(As[i]) - Bs[i][0][0] )
    eq11.append( f11(As[i]) - Bs[i][1][1] )
    eq22.append( f22(As[i]) - Bs[i][2][2] )
    eq33.append( f33(As[i]) - Bs[i][3][3] )

F.<x00, x10, x20, x30> = PolynomialRing(GF(251))
I = F.ideal(eq00)
S00 = I.variety()

F.<x01, x11, x21, x31> = PolynomialRing(GF(251))
I = F.ideal(eq11)
S11 = I.variety()

F.<x02, x12, x22, x32> = PolynomialRing(GF(251))
I = F.ideal(eq22)
S22 = I.variety()

F.<x03, x13, x23, x33> = PolynomialRing(GF(251))
I = F.ideal(eq33)
S33 = I.variety()

print(prod(map(len, (S00, S11, S22, S33))))

A = matrix(GF(251), As[0])
B = matrix(GF(251), Bs[0])

for S0 in S00:
    XT = [[0 for _ in range(4)] for _ in range(4)]
    XT[0] = [S0[i] for i in [x00, x10, x20, x30]]
    for S1 in S11:
        XT[1] = [S1[i] for i in [x01, x11, x21, x31]]
        for S2 in S22:
            XT[2] = [S2[i] for i in [x02, x12, x22, x32]]
            for S3 in S33:
                XT[3] = [S3[i] for i in [x03, x13, x23, x33]]
                _XT = matrix(GF(251), XT)
                if _XT * A * _XT.T == B:
                    X = str(_XT.T.list())[1:-1]
                    io.sendlineafter(b" > ", X.encode())
                    exit(io.recvline().decode()[:-1])
