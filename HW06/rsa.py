#!/usr/bin/env python
#!/usr/bin/env python -W ignore::DeprecationWarning

#HW06
#Matteo G. Miglio
#ECN Login: miglio@purdue.edu
#Due Date: 03/09/2021

import sys
from BitVector import *
from PrimeGenerator import *

#Binary greatest common divisor algorithm (bitwise operations have a much faster runtime that inplace, base10 operations) - Credit Avi Kak
def bgcd(a,b):
    if a == b: return a                                         #(A)
    if a == 0: return b                                         #(B)
    if b == 0: return a                                         #(C)
    if (~a & 1):                                                #(D)
        if (b &1):                                              #(E)
            return bgcd(a >> 1, b)                              #(F)
        else:                                                   #(G)
            return bgcd(a >> 1, b >> 1) << 1                    #(H)
    if (~b & 1):                                                #(I)
        return bgcd(a, b >> 1)                                  #(J)
    if (a > b):                                                 #(K)
        return bgcd( (a-b) >> 1, b)                             #(L)
    return bgcd( (b-a) >> 1, a )                                #(M)

def generate_p_q(outputF_p, outputF_q, e):
    num_of_bits_desired = 128 #need Bits/2 size of p, q
    generator = PrimeGenerator( bits = num_of_bits_desired ) #create an object
    p_file = open(outputF_p, 'w')
    q_file = open(outputF_q, 'w')
    #create an instance of the prime generator class
    generator = PrimeGenerator( bits = num_of_bits_desired ) #create an object
    while True:
        #generate two random numbers p and q
        p_as_int = generator.findPrime()
        q_as_int = generator.findPrime()
        #turn into binary in order to validate that the 2 most significant bits are set (acts similar to string indexing)
        p_as_b2 = bin(p_as_int)
        q_as_b2 = bin(q_as_int)
        #2 leftmost bits are set
        if (p_as_b2[(0+2)]==0 or p_as_b2[(1+2)]==0 or q_as_b2[(0+2)]==0 or q_as_b2[(1+2)]==0): continue
        #check if they are equal
        if p_as_int == q_as_int: continue
        #ensure that the gcd == 1 in order to be comprime to e.
        if (bgcd(p_as_int-1, e)==1 and bgcd(q_as_int-1, e)==1): break
    #add to the files
    print(p_as_int)
    print(q_as_int)
    p_file.write(str(p_as_int))
    q_file.write(str(q_as_int))
    p_file.close()
    q_file.close()
    return

'''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-DECRYPTION=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=
'''
def decrypt(encryptedF, p, q, e, decryptedF):
    #This decryption funtion mostly derives form the CRT method used in lecture notes 12.5
    with open(p, 'r') as p_f:
        p = p_f.readline()
        p = int(p)
    with open(q, 'r') as q_f:
        q = q_f.readline()
        q = int(q)
    #calculate n modulus
    n  = p * q
    #totient is number of coprimes <n
    totient = (p-1)*(q-1)
    totient_bv = BitVector(intVal = totient)

    e_bv = BitVector(intVal = e)
    #find the private key which is the inverse of e with respect to the totient of the public key
    d_int = e_bv.multiplicative_inverse(totient_bv).int_val()

    p_bv = BitVector(intVal = p)
    q_bv = BitVector(intVal = q)
    #Xp = q × (q^−1 mod p)
    p_q_bv = q_bv.multiplicative_inverse(p_bv)
    x_p = q * (p_q_bv.int_val())
    #Xq = p × (q^−1 mod q)
    q_p_bv = p_bv.multiplicative_inverse(q_bv)
    x_q = p * (q_p_bv.int_val())

    
    with open(encryptedF, 'r') as IP:
        input_bv = BitVector(hexstring = IP.read())
    message = ""
    encryptedFileLen = len(input_bv)
    print(encryptedFileLen)
    for blkSize in range(256, encryptedFileLen+1, 256):
        #take 256 chunks to read in
        C = input_bv[blkSize-256:blkSize]
        #calculate V_p and V_q for the CRT
        v_p = pow(int(C.int_val()), d_int, p)
        v_q = pow(int(C.int_val()), d_int, q)
        #decrypt the integer vis-a-vis the public key modulus
        decrypted_int = (((v_p)*(x_p) + (v_q)*(x_q)) % n)
        #put back into bitvector to take the ascii interpretation
        decrypted_bv = BitVector(intVal = decrypted_int, size = 256)
        #Ignore the zeros that were padded from the left 
        dec_short = decrypted_bv[128:256]
        #ignore null terminator
        message += dec_short.get_bitvector_in_ascii().strip('\0')
    with open(decryptedF, "w") as outF:
        outF.write(message)
    return

'''

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-ENCRYPTION=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=
'''
def encrypt(messageF, p, q, e, encryptedF):
    with open(p, 'r') as p_f:
        p = p_f.readline()
        p = int(p)
    with open(q, 'r') as q_f:
        q = q_f.readline()
        q = int(q)

    outputF = open(encryptedF, 'w')

    #calculate n modulus
    n  = p * q
    #totient is number of coprimes <n
    totient = (p-1)*(q-1)
    input_bv = BitVector(filename = messageF)
    while (input_bv.more_to_read):
        #read 128 bits at a time from the file
        data = input_bv.read_bits_from_file(128)
        if (data.length() < 128):
            #pad fromthe left to make sure that it =128
            data.pad_from_right(128-data.length())
        #pad from the left to get 256 bits
        data.pad_from_left(128)
        #BitVector->int
        data_as_int = data.int_val()
        #take modulus power to reduce runtime and cypther the text
        cipher_text_as_int = pow(data_as_int, e, n)
        #extend it to  256 to make sure thesize is correct
        cipher_text_bv = BitVector(intVal = cipher_text_as_int, size = 256)
        outputF.write(cipher_text_bv.get_bitvector_in_hex())
    outputF.close()
    return
'''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=main-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=
'''
if __name__ == '__main__':
    if sys.argv[1] == '-g':
    #generate the random numbers p,q.
        generate_p_q(sys.argv[2], sys.argv[3], 65537)
    elif sys.argv[1] == '-e':
        encrypt(sys.argv[2], sys.argv[3], sys.argv[4], 65537, sys.argv[5])
    elif sys.argv[1] == '-d':
        decrypt(sys.argv[2], sys.argv[3], sys.argv[4], 65537, sys.argv[5])

