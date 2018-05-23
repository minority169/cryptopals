from Crypto.Cipher import AES
from binascii import a2b_base64

def AES_128_ECB_decrypt(msg, key):
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.decrypt(msg)

key = 'YELLOW SUBMARINE'
file = open('input.txt', 'r')
msg = a2b_base64(''.join(file.read().split('\n')))
print(AES_128_ECB_decrypt(msg, key).decode('ascii'))
