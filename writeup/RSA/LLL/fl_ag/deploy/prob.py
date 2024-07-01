from Crypto.Util.number import getPrime, GCD, bytes_to_long

while True:
    p = getPrime(1024)
    q = getPrime(1024)
    e = 0x101
    if GCD((p - 1) * (q - 1), e) == 1:
        break
N = p * q

with open('flag', 'rb') as f:
    flag = f.read()
    assert len(flag) == 68

fl, ag = flag[:34], flag[34:]
fl, ag, flag = map(bytes_to_long, (fl, ag, flag))

fl_enc = pow(fl, e, N)
ag_enc = pow(ag, e, N)
flag_enc = pow(flag, e, N)

print(f"{N = }")
print(f"{e = }")
print(f"{fl_enc = }")
print(f"{ag_enc = }")
print(f"{flag_enc = }")