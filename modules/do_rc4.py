#!/usr/bin/python
#
### Info: Applies RC4 crypto key to input.
### Required args: A key in hex format (no spaces or leading 0x) is required.

from binascii import unhexlify
def convert(data, args):

	#rc4 Gen s-Box
	s = []
	for i in range(0,256):
		s.append(i)

	key = unhexlify(args[0])
	j = 0
	for i in range ( 0,256 ):
		j = (j + s[i] + ord(key[i % len(key)])) % 256
		s[i],s[j] = s[j],s[i]

	i = 0
	j = 0

	Ciphertext = []
	for x in data:
		i = ( i + 1 ) % 256
		j = ( j + s[i]) % 256
		s[i],s[j] = s[j],s[i]
		K = s[ ( s[i] + s[j] ) % 256]
	
		# Create List of Resulting Ciphertext
		Ciphertext.insert(len(Ciphertext), chr((ord(x) ^ K)))

	return [''.join(Ciphertext)]
