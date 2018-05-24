def extend_block(msg, block_size = 10):
	to_add = (block_size - (len(msg) % block_size)) % block_size
	msg += chr(to_add) * to_add
	return msg

msg = input()
print(extend_block(msg).encode('ascii'))
