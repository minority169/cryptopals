from Crypto import Random
from Crypto.Cipher import AES
from random import randint

def gen_random_key(keysize = 16):
	return Random.new().read(keysize)

def extend_block(msg, block_size):
	to_add = (block_size - (len(msg) % block_size)) % block_size
	msg += bytes([to_add]) * to_add
	return msg

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

def encrypt_with_random_key(msg, keysize = 16):
	key = gen_random_key(keysize)
	msg = Random.new().read(randint(5, 10)) + msg.encode('ascii')
	msg += Random.new().read(randint(5, 10))
	msg = extend_block(msg, keysize)
	if (randint(0, 1) == 1):
		iv = gen_random_key(keysize)
		return AES_128_CBC_encrypt(msg, key, iv)
	else:
		return AES_128_ECB_encrypt(msg, key)

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
	cipher = encrypt_with_random_key(msg * 32, keysize)
	if (get_AES_ECB_score(cipher, keysize) > 0):
		return 'ECB'
	else:
		return 'CBC'


for i in range(10):
	msg = input()
	print(mode_detection_oracle(msg))
