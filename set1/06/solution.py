from binascii import a2b_base64, unhexlify

freq = {
	'a': 0.0651738,
    'b': 0.0124248,
    'c': 0.0217339,
    'd': 0.0349835,
    'e': 0.1041442,
    'f': 0.0197881,
    'g': 0.0158610,
    'h': 0.0492888,
    'i': 0.0558094,
    'j': 0.0009033,
    'k': 0.0050529,
    'l': 0.0331490,
    'm': 0.0202124,
    'n': 0.0564513,
    'o': 0.0596302,
    'p': 0.0137645,
    'q': 0.0008606,
    'r': 0.0497563,
    's': 0.0515760,
    't': 0.0729357,
    'u': 0.0225134,
    'v': 0.0082903,
    'w': 0.0171272,
    'x': 0.0013692,
    'y': 0.0145984,
    'z': 0.0007836,
    ' ': 0.1918182
}

def text_score(text):
	score = 0
	for letter in text:
		if chr(letter) in freq:
			score += freq[chr(letter)]
	return score

def break_single_byte_XOR(cipher):
	best_score = 0
	ans = cipher
	secret_key = 0
	for key in range(256):
		text = b''
		for byte in cipher:
			text += bytes([byte ^ key])
		if (text_score(text) > best_score):
			best_score = text_score(text)
			ans = text
			secret_key = key
	return (ans.decode('ascii'), secret_key)

def hamming_distance(a, b):
	dist = 0
	for i in range(len(a)):
		byte1 = a[i]
		byte2 = b[i]
		for j in range(8):
			dist += abs(byte1 % 2 - byte2 % 2)
			byte1 //= 2
			byte2 //= 2
	return dist

def get_keysize(msg):
	result = [(0, 0)] * 38
	for keysize in range(2, 40):
		score = 0
		for i in range(len(msg) // keysize - 1):
			score += hamming_distance(msg[i * keysize:(i + 1) * keysize],
				msg[(i + 1) * keysize:(i + 2) * keysize]) / keysize
		score /= len(msg) // keysize - 1
		result[keysize - 2] = (score, keysize)
	return sorted(result)

def get_blocks(msg, keysize):
	blocks = [b''] * keysize
	for i in range(len(msg)):
		blocks[i % keysize] += bytes([msg[i]])
	return blocks

file = open('input.txt', 'r')
cipher = file.read().split('\n')
cipher = ''.join(cipher)
msg = a2b_base64(cipher)
scores = get_keysize(msg)
blocks = get_blocks(msg, scores[0][1])

key = ''
for i in range(len(blocks)):
	decoded = break_single_byte_XOR(blocks[i])
	blocks[i] = decoded[0]
	key += chr(decoded[1])

print("SECRET KEY:", key)
for i in range(len(blocks[0])):
	for j in range(len(blocks)):
		if (i < len(blocks[j])):
			print(blocks[j][i], end = '')