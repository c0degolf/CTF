n = 0x1efa18c18112a71bcaa1614fec91a84441270fab3fc5fc80d574681e829f79bc7795d61c0a719042995f41dae71e0da17fc44319d51d7ea7b3b6770664a85726a0bf4d48ab85e0ae4049938170cffdc13fa97e2796953d2d7a7d02dc16a19a2ad7597968fc3d3edfcda78c4b38e378b58bb3853fa1fdd1961cdc248eeac3cfc3353f89ea92280b6878828b93e71dd920c5f9f64b86111b3cdebb77d2a19b2adb697cec628626de6c9662f8bbe5a06e0b608c84798d5d3dd7d50cd64c2777eb2fe954b6d4e728d754dbacb524df00b538ba777272673efec499f4585f7704af0cb92e2643fbcf4d22e6cbdd71f3aa27de955a1e7c6a7f846165339858f989054f910d0aa393a1389df8eaea5b877f87abcbe6c1833b93234ae98558f5a216c70469dfabe467e4a60b8f5589a0683cf67b4a65830cc72067fce328c5ade4a7fb9d6e95ee09deeb7f3440099e479610b642b4b49b43cd6d608946b61071550a58fb62bc8d0d0c38bce5a683fe79d05bfd8ec6b94209e69fcb53330575998ffe47a83e092541e88c6040575561ff9960deeaddd53902e11d3076bbd86ae0c30f28f3dd4531c8793dc2283800f9486b03e7f134a88466e949ccff7dcc283dccf937f41a974eae243d7d6608604e2644e2256bcd3f71357c5202fb1c0f52946aa713f4677c763129ea5ccf84baffc336c989db1876d13f8a9f6bc68e0ac8ee490f8aa4f
c = 0xc8848a1137b849c881d4635f7b00518bfcfe91099a30675bb044c39c5df6846c95f44373e53c9adae4cafe2cde74b30e6005d93fd0593206b026584b17cd4d0997d5657c74341f17e68e19c30abbd4158ab4d169a35052003db3e4044530e8d26ddb3d3a0cecc4c520cf3ed681a89870965c7403cc7aff24935f347998f0dcf4108d06e5d9f922d0fc11e14b7ad582828c3c743b7142f7f756131324a0ca055dbd2853c5fb136ae21ae35941e6b018756e4bc27838d13122db597ed27d41784b561d0592a87134ad48fa5e248530c3c5d67cd2a79845f31e1dff79018666d0b9013cd2976bd1b2f6843ecc5991211e8b4ccdbd4a66f2f761d8e7cb655c19ccd2506d90b6f705f223b9cc25d2fc4a6651272f671c7a180617ea98dd3b9f3d7756e990f6b563167f847ce6dac1b57c0a67b3d1913734665b3a2b706fa78cdc741f40ef6b543212d5e04be52c001f0c2bafd81dc5f000adc1ba2c9190ee6a4a41b5c005f68422f6860033ed71eec811d8fc4bb51f0840ada0c6c713ab96e7e02c088bb12a532c40282a237d3a66a8a8ed72b712823dfaf2a0fd7451cc711ad1050f0b8599f00be0256b3f280a53cef61ff80efe54e6fbd593b3b268afac3d5bc36b85824789d2009c6a6cefc6a66acb58247ffb45a1787542c2872ee374129e972028a004b9f89386c2ad4415005d830131054674721b528966c297e181284721db
e = 0x10001

F.<x> = GF(2)[]
npol = F([*map(int, bin(n)[2:])][::-1])
cpol = F([*map(int, bin(c)[2:])][::-1]) # 씨폴
phi = 1

for fac, cnt in list(npol.factor()):
    phi *= (2^fac.degree()-1)^cnt

d = pow(e, -1, phi)

raise ZeroDivisionError(__import__('re').search(b'DH{.*}', int(''.join(map(str, list(pow(cpol, d, npol))[::-1])), 2).to_bytes(5100, 'big')).group().decode())