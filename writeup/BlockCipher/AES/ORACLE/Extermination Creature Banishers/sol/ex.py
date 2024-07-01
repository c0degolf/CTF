from pwn import *
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from tqdm import tqdm

# context.log_level = True

p = remote("host3.dreamhack.games", 14692)

name = (16-len('{"user_name": "'))*b"_"+b"A"*32+b"critical_attack_"+b"_"*(16-(len('", "creature_info": {"name": "Demonlord", "critical": "')%16))
p.sendlineafter(b"> ", name)

for n in range(10):
    aes_mode = 2
    while aes_mode == 2:
        p.recvuntil(b"<Stage Status>\n")
        hint = b64decode(p.recvline()[:-1])
        aes_mode = AES.MODE_ECB if hint[16:32]==hint[32:48] else AES.MODE_CBC

        p.recvuntil(b"Wild ")
        creature_name = p.recvline().split()[0]

        p.sendlineafter(b"1. Fight    2. Run\n", f"{aes_mode}".encode())

    payload = b"critical_attack_"
    fixed = 1
    letters = [*b"0123456789abcdef"]

    for t in tqdm(range(16)):
        for i in letters:
            maybe = (b"__" + payload[fixed:] + bytes([i]))

            assert len(maybe) == 18

            maybe += b"_"*(32-(len(b'{"user_cmd": "", "creature_info": {"name": "", "critical": "'+creature_name+maybe)%16)-fixed)
            
            p.sendlineafter(b"Attack Command: ", maybe)

            p.recvuntil(b"<Fight Status>\n")
            tmp = b64decode(p.recvline()[:-1])

            if tmp[32:].find(tmp[16:32]) != -1:
                payload += bytes([i])
                fixed += 1
                break

    p.sendlineafter(b"Attack Command: ", payload)
    print(n+1, payload)

p.recvuntil(b"Well done!\n")
print(p.recvline()[:-1].decode())