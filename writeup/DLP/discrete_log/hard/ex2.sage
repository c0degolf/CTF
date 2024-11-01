# Not My Code

from pwn import *
import random
from Crypto.Util.number import *
from tqdm import tqdm, trange

res = []
mod = []

nice = []

q = getPrime(1000)

st = (2^1024 - 1) // (q * 2)

while True:
	if isPrime(int(st * q * 2 + 1)):
		nice.append(st)

		print(len(nice))

	st -= 1

	if len(nice) == 77:
		break

assert int(lcm(nice)).bit_length() > 1100


io = process(["python3", "prob_revenge.py"])
# io = remote("43.201.97.135", 3667)

mod = []
res = []

for i in trange(77):
	dlog = nice[i]
	p = 2 * q * dlog + 1

	io.sendlineafter("> ", hex(p))
	io.sendlineafter("> ", hex(q))

	io.recvuntil("g = ")
	gg = ZZ(int(io.recvline()[:-1].decode(), 16))
	io.recvuntil("x = ")
	ggx = ZZ(int(io.recvline()[:-1].decode(), 16))

	order = p - 1

	assert pow(gg, order, p) == 1
	assert pow(ggx, order, p) == 1

	for fac in dlog.factor():
		pp = fac[0]

		if pp in mod:
			continue

		order = pp
		g = pow(gg, (p - 1) // pp, p)
		gx = pow(ggx, (p - 1) // pp, p)

		# print(g, gx)
		if g == 1:
			continue

		assert pow(g, pp, p) == 1
		assert pow(gx, pp, p) == 1

		step = round(ZZ(order).sqrt())

		smolstep = []
		bigstep = []

		st = 1

		for i in range(step):
			smolstep.append(st)
			st *= g
			st %= p

		st = gx
		heh = pow(g, step, p)

		for i in range(step):
			bigstep.append(st)
			st /= heh
			st %= p

		bigstepset = set(bigstep)

		found = False

		for i in range(step):
			if smolstep[i] in bigstepset:
				a = i
				found = True
				break

		if not found:
			continue

		for i in range(step):
			if smolstep[a] == bigstep[i]:
				b = i
				break

		hehe = step * b + a

		assert pow(g, hehe, p) == gx

		mod.append(pp)
		res.append(hehe)

flag = crt(res, mod)

assert int(prod(mod)).bit_length() > 1030

# print(flag.bit_length())

print(long_to_bytes(flag))




