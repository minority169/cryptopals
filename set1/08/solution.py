from binascii import unhexlify

def get_AES_ECB_score(msg, block_size = 16):
	blocks_num = len(msg) // block_size - 1
	score = 0
	for i in range(blocks_num):
		for j in range(i + 1, blocks_num):
			if (msg[i * block_size:(i + 1) * block_size] ==
				msg[j * block_size:(j + 1) * block_size]):
				score += 1
	return score

file = open('input.txt', 'r')
for line in file:
	if (get_AES_ECB_score(line.strip()) > 0):
		print(line.strip())
