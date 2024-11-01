from output import pub, enc
from Crypto.Util.number import long_to_bytes

n = len(pub)

N = ceil(1/2 * n**0.5)
M = matrix(QQ, n+1, n+1)

for i in range(n):
    M[i, i] = 1
    M[n, i] = -1/2
    M[i, n] = N*pub[i]

M[n, n] = -N*enc

for row in M.LLL():
    row = row[:-1][::-1]
    res = ""
    for r in row: res += str(int(r+1/2))

    try:
        print(long_to_bytes(int(res, 2)))
    except:
        continue