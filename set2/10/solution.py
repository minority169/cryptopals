from Crypto.Cipher import AES
from binascii import a2b_base64

def extend_block(msg, block_size):
	to_add = (block_size - (len(msg) % block_size)) % block_size
	msg += bytes([to_add]) * to_add
	return msg

def AES_128_ECB_decrypt(msg, key):
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.decrypt(msg)

def AES_128_ECB_encrypt(msg, key):
	msg = extend_block(msg, len(key))
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(msg)

def str_xor(a, b):
	result = b''
	for i in range(len(a)):
		result += bytes([a[i] ^ b[i]])
	return result

def AES_128_CBC_encrypt(msg, key, iv):
	cipher = extend_block(msg, len(key))
	blocks_cnt = len(cipher) // len(key)
	encoded = b''
	prev_block = iv
	for i in range(blocks_cnt):
		cur_block = msg[i * len(key):(i + 1) * len(key)]
		cur_block = str_xor(cur_block, prev_block)
		encrypted_block = AES_128_ECB_encrypt(cur_block, key)
		encoded += encrypted_block
		prev_block = encrypted_block
	return encoded

def AES_128_CBC_decrypt(cipher, key, iv):
	blocks_cnt = len(cipher) // len(key)
	decoded = b''
	prev_block = iv
	for i in range(blocks_cnt):
		cipher_block = cipher[i * len(key):(i + 1) * len(key)]
		decrypted_block = AES_128_ECB_decrypt(cipher_block, key)
		decoded += str_xor(prev_block, decrypted_block)
		prev_block = cipher_block
	return decoded

key = b'YELLOW SUBMARINE'
iv = b'ABABABABABABABAB'
msg = b'AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBB'
cipher = AES_128_CBC_encrypt(msg, key, iv)
print(AES_128_CBC_decrypt(cipher, key, iv))

key = b'YELLOW SUBMARINE'
iv = b'\x00' * len(key)
file = open('input.txt', 'r')
cipher = a2b_base64(''.join(file.read().split('\n')))
print(AES_128_CBC_decrypt(cipher, key, iv).decode('ascii'))
