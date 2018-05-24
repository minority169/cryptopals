from Crypto import Random
from Crypto.Cipher import AES
from random import randint
from binascii import a2b_base64

def gen_random_key(keysize = 16):
	return Random.new().read(keysize)

secret_key = gen_random_key()
file = open('input.txt', 'r')
secret_padding = a2b_base64(file.read())

def extend_block(msg, block_size):
	to_add = (block_size - (len(msg) % block_size)) % block_size
	msg += bytes([to_add]) * to_add
	return msg

def AES_128_ECB_encrypt(msg, key):
	msg = extend_block(msg, len(key))
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(msg)

def encrypt_with_padding(msg, keysize = 16):
	msg = msg + secret_padding
	return AES_128_ECB_encrypt(msg, secret_key)

def get_AES_ECB_score(msg, block_size = 16):
	blocks_num = len(msg) // block_size
	score = 0
	for i in range(blocks_num):
		for j in range(i + 1, blocks_num):
			if (msg[i * block_size:(i + 1) * block_size] ==
				msg[j * block_size:(j + 1) * block_size]):
				score += 1
	return score

def mode_detection_oracle(msg, keysize = 16):
	cipher = encrypt_with_padding(msg.encode('ascii') * 32, keysize)
	if (get_AES_ECB_score(cipher, keysize) > 0):
		return 'ECB'
	else:
		return 'CBC'

def find_block_size():
	prev = len(AES_128_ECB_encrypt(b'A', secret_key))
	cur = len(AES_128_ECB_encrypt(b'AA', secret_key))
	cnt = 2
	while (cur == prev):
		cnt += 1
		prev = cur
		cur = len(AES_128_ECB_encrypt(b'A' * cnt, secret_key))
	return cur - prev

def decrypt_padding(block_size):
	partial_block = b'A' * (block_size - 1)
	plaintext = b''
	for i in range(len(secret_padding)):
		right_cipher = encrypt_with_padding((i + 1) * partial_block)[:(i + 1) * block_size]
		for byte in range(256):
			cur_block = (i + 1) * partial_block + plaintext + bytes([byte])
			if (encrypt_with_padding(cur_block)[:(i + 1) * block_size] == right_cipher):
				plaintext += bytes([byte])
				break
	return plaintext

block_size = find_block_size()
print(block_size)
print(mode_detection_oracle('ABCDEFG', block_size))
print(decrypt_padding(block_size).decode('ascii'))
