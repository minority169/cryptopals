from binascii import unhexlify

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
	for key in range(256):
		text = b''
		for byte in cipher:
			text += bytes([byte ^ key])
		if (text_score(text) > best_score):
			best_score = text_score(text)
			ans = text
	return ans

file = open('input.txt', 'r')
best_score = 0
ans = 0
for line in file:
    cur = unhexlify(line[:-1])
    decoded = break_single_byte_XOR(cur)
    if (text_score(decoded) > best_score):
        best_score = text_score(decoded)
        ans = decoded
print(ans.decode('ascii'))

