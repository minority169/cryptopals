from binascii import b2a_base64, a2b_hex

print(b2a_base64(a2b_hex(input())).decode('ascii'))
