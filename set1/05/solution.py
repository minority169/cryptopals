from binascii import hexlify

KEY = 'ICE'

def encode_repeated_XOR(msg, key):
    ind = 0
    cipher = b''
    for byte in msg:
        cipher += bytes([ord(byte) ^ ord(key[ind % len(key)])])
        ind += 1
    return cipher

file = open('input.txt', 'r')

print(hexlify(encode_repeated_XOR(file.read(), KEY)).decode('ascii'))
