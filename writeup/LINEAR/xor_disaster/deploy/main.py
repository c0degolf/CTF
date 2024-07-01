from disaster import *

def main():
    inp = input('> ')
    assert len(inp) == 68
    assert inp[:3] == 'DH{' and inp[-1] == '}'
    v = int(inp[3:-1], 16)
    assert xor0(v) == 246
    assert xor1(v) == 44
    assert xor2(v) == 115
    assert xor3(v) == 230
    assert xor4(v) == 101
    assert xor5(v) == 35
    assert xor6(v) == 204
    assert xor7(v) == 151
    assert xor8(v) == 20
    assert xor9(v) == 200
    assert xor10(v) == 112
    assert xor11(v) == 111
    assert xor12(v) == 231
    assert xor13(v) == 74
    assert xor14(v) == 41
    assert xor15(v) == 189
    assert xor16(v) == 95
    assert xor17(v) == 22
    assert xor18(v) == 222
    assert xor19(v) == 90
    assert xor20(v) == 58
    assert xor21(v) == 130
    assert xor22(v) == 0
    assert xor23(v) == 172
    assert xor24(v) == 1
    assert xor25(v) == 236
    assert xor26(v) == 89
    assert xor27(v) == 243
    assert xor28(v) == 80
    assert xor29(v) == 113
    assert xor30(v) == 242
    assert xor31(v) == 112
    print(f'flag is {inp}')

if __name__ == "__main__":
    main()
