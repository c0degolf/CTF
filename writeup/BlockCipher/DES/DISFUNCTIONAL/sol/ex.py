from pwn import *
from tqdm import tqdm

context.log_level = 'error'

while True:
    p = remote("desfunctional.2024.ctfcompetition.com", 1337)

    p.sendlineafter(b"flag\n", b"1")
    enc = bytes.fromhex(p.recvline(keepends=False).decode())
    enc = xor(enc, b'\xff'*64)

    for _ in tqdm(range(9)):
        p.sendlineafter(b"flag\n", b"2")
        p.sendlineafter(b"ct: ", enc.hex().encode())
        dec = bytes.fromhex(p.recvline(keepends=False).decode())

    p.sendlineafter(b"flag\n", b"3")
    chall = xor(dec[:8], b'\xff'*8) + dec[8:]
    p.sendlineafter(b"pt: ", chall.hex().encode())

    flag = p.recvline()
    if flag.find(b"CTF") != -1: 
        import re
        flag = re.search('CTF{.*}', flag.decode()).group()
        raise ZeroDivisionError(flag)
    
# sol             = 00111110011000000111011011011111100010011100111100011101010110111101111100110000101000100010000101110111111110001001000111001001100100001001100111010100011110101010111100011110001010001100110100000010100100011111100001110110111001011100100111011010001110001111111111101111010101101000101101111000000010001100110110001111110011111111100100010100111010011100110010101100100011111100100101000000000101111011001110111100110101010100011101000011101011100001010010110111001000100000100101111000010110111110111100001010
# enc             = 10000101000111001011101001110111110111010110110100000100000101011011101000101100110110010110000000001010111000111010110110111110111110011101000101100011101001111100111100011010110000111001100011100011110001101000101010000010000011000101000100110111100101010001001011011100110010000110011001111011100100111000010010111110000010110000110101111101101100100110111001110000110110100001000001101010111110000111101001111001001110100010000010010111111100001001001001100011111111010101011000010110000101100110110001010110
# enc_xor         = 01111010111000110100010110001000001000101001001011111011111010100100010111010011001001101001111111110101000111000101001001000001000001100010111010011100010110000011000011100101001111000110011100011100001110010111010101111101111100111010111011001000011010101110110100100011001101111001100110000100011011000111101101000001111101001111001010000010010011011001000110001111001001011110111110010101000001111000010110000110110001011101111101101000000011110110110110011100000000101010100111101001111010011001001110101001
# dec_enc_xor     = 11000001100111111000100100100000011101100011000011100010101001001101111100110000101000100010000101110111111110001001000111001001100100001001100111010100011110101010111100011110001010001100110100000010100100011111100001110110111001011100100111011010001110001111111111101111010101101000101101111000000010001100110110001111110011111111100100010100111010011100110010101100100011111100100101000000000101111011001110111100110101010100011101000011101011100001010010110111001000100000100101111000010110111110111100001010
# dec_enc_xor_xor = 00111110011000000111011011011111100010011100111100011101010110110010000011001111010111011101111010001000000001110110111000110110011011110110011000101011100001010101000011100001110101110011001011111101011011100000011110001001000110100011011000100101110001110000000000010000101010010111010010000111111101110011001001110000001100000000011011101011000101100011001101010011011100000011011010111111111010000100110001000011001010101011100010111100010100011110101101001000110111011111011010000111101001000001000011110101