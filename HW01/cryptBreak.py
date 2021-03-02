#HW01
#Matteo Miglio
#miglio@purdue.edu
#01/28/2021
#!/usr/bin/env python3

import sys
from BitVector import *

BLOCKSIZE = 16
numbytes = BLOCKSIZE // 8
#key_bv = BitVector(intVal=someRandomInteger, size=16)
PassPhrase = "Hopes and dreams of a million years"

#Arguments:
# ciphertextFile: String containing file name of the ciphertext (e.g. encrypted.txt )
# key_bv: 16-bit BitVector of the key used to try to decrypt the ciphertext.#Function Description:
# Attempts to decrypt ciphertext contained in ciphertextFile using key_bv and returnsthe original plaintext as a string
def cryptBreak(ciphertextFile,key_bv):
	bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                  
	for i in range(0,len(PassPhrase) // numbytes):                         
	    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]
	    bv_iv ^= BitVector( textstring = textstr )

	msg_decrypted_bv = BitVector( size = 0 )
	previous_decrypted_block = bv_iv
	for i in range(0, len(encrypted_bv) // BLOCKSIZE):
		bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
		temp = bv.deep_copy()
		bv ^=  previous_decrypted_block
		previous_decrypted_block = temp
		bv ^=  key_bv
		msg_decrypted_bv += bv
	outputtext = msg_decrypted_bv.get_text_from_bitvector()
	return outputtext

if __name__ == "__main__":
	FILEIN = open(sys.argv[1])
	encrypted_bv = BitVector(hexstring = FILEIN.read())
	for key in range(2**(BLOCKSIZE)):
		key_bv = BitVector(intVal = key, size = BLOCKSIZE)
		test_msg = cryptBreak(encrypted_bv, key_bv)
		if 'Yogi Berra' in test_msg:
			print('Encryption Broken!')
			print('The encryption key is: ' + str(key))
			FILEOUT = open(sys.argv[2], 'w')
			FILEOUT.write(test_msg)
			FILEOUT.close()
			sys.exit()
