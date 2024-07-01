import hashlib
from Crypto.Cipher import AES
from tqdm import tqdm

p = 310717010502520989590157367261876774703
a = 2
b = 3
E = EllipticCurve(GF(p), [a,b])

g_x = 179210853392303317793440285562762725654
g_y = 105268671499942631758568591033409611165
G = E(g_x, g_y)

b_x = 272640099140026426377756188075937988094
b_y = 51062462309521034358726608268084433317
B = E(b_x, b_y)

# pub = G*n
P = E(280810182131414898730378982766101210916, 291506490768054478159835604632710368904)

primes = []
for i in factor(P.order()):
    primes.append(i[0]**i[1])

dlogs = []
for i in tqdm(primes):
    t = int(G.order() / i)
    dlog = discrete_log(t*P, t*G, operation = '+')
    dlogs.append(dlog)

n = crt(dlogs, primes)

key = (B*n)[0]
sha1 = hashlib.sha1()
sha1.update(str(key).encode('ascii'))
key = sha1.digest()[:16]

info = {'iv': '07e2628b590095a5e332d397b8a59aa7', 'ct': '8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af'}

cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(info['iv']))
print(cipher.decrypt(bytes.fromhex(info['ct'])).decode().strip())