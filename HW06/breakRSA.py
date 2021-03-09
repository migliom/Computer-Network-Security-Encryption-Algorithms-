#!/usr/bin/env python
#!/usr/bin/env python -W ignore::DeprecationWarning

#HW06
#Matteo G. Miglio
#ECN Login: miglio@purdue.edu
#Due Date: 03/09/2021

from BitVector import *
from PrimeGenerator import *
from solve_pRoot_BST import *
import sys

'''for this HW, we have set our e value to be the smallest value such that it is prime and easy to use the CRT method 
    to crack the encryption without using the private key'''
e = 3
e_bv = BitVector(intVal = e)
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

def generate_p_q():
    n_list = []
    p_list = []
    q_list = []
    num_of_bits_desired = 128 #need Bits/2 size of p, q
    for i in range(0,3,1):
        generator = PrimeGenerator( bits = num_of_bits_desired ) #create an object
        while True:
            p_as_int = generator.findPrime()
            q_as_int = generator.findPrime()
            p_as_b2 = bin(p_as_int)
            q_as_b2 = bin(q_as_int)
            #2 leftmost bits
            if (p_as_b2[(0+2)]==0 or p_as_b2[(1+2)]==0 or q_as_b2[(0+2)]==0 or q_as_b2[(1+2)]==0): continue
            if p_as_int == q_as_int: continue
            if (bgcd(p_as_int-1, e)==1 and bgcd(q_as_int-1, e)==1): break
        n = p_as_int * q_as_int
        n_list.append(n)
        p_list.append(p_as_int)
        q_list.append(q_as_int)
        d = e_bv.multiplicative_inverse((BitVector(intVal = n)))
    return n_list, p_list, q_list
'''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=Encrypt=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
'''
def encrypt(messageF,n, p, q, inputF):
    encF = open(inputF, 'w')
    #calculate n modulus
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
        encF.write(cipher_text_bv.get_bitvector_in_hex())
    encF.close()
    return

def read_n_file(in_file):
    #read line by line and take in all the public keys
    public_key_list = []
    with open(in_file, 'r') as n_File:
        public_key_list.append(int(n_File.readline()))
        public_key_list.append(int(n_File.readline()))
        public_key_list.append(int(n_File.readline()))
    return  public_key_list

def decrypt(n_list, encF1, encF2, encF3, outputF):
    '''Since n1,n2 and n3 are pairwise co-prime, CRT allowsus to reconstruct M^3 modulo N = n1*n2*n3. This will require us to find Ni = N/ni for all i. Then find the multiplicative inverse of each Ni vis-a-vis each ni modulo. We can recover M^3 = (C1 * N1 * N1_inv + ... + Ci * Ni * ni_inv).
    '''
    #Ni = N / Ni
    N = n_list[0] * n_list[1] * n_list[2]
    #Just multply instead of adding to avoid the float issue -> Calculate Ni
    N1 = n_list[1] * n_list[2]
    N2 = n_list[0] * n_list[2]
    N3 = n_list[0] * n_list[1]
    #calculate the inverse of Ni with respect to the corresponding n value
    N1_inv = BitVector(intVal = N1).multiplicative_inverse(BitVector(intVal = n_list[0])).int_val()
    N2_inv = BitVector(intVal = N2).multiplicative_inverse(BitVector(intVal = n_list[1])).int_val()
    N3_inv = BitVector(intVal = N3).multiplicative_inverse(BitVector(intVal = n_list[2])).int_val()

    with open(encF1, 'r') as IP:
        input1_bv = BitVector(hexstring = IP.read())
    with open(encF2, 'r') as IP:
        input2_bv = BitVector(hexstring = IP.read())
    with open(encF3, 'r') as IP:
        input3_bv = BitVector(hexstring = IP.read())

    encryptedFileLen = len(input1_bv)
    message = ""
    for blkSize in range(256, encryptedFileLen+1, 256):
        #take chunks of the cipher text file in 256 bit chunks
        C1 = input1_bv[blkSize-256:blkSize].int_val()
        C2 = input2_bv[blkSize-256:blkSize].int_val()
        C3 = input3_bv[blkSize-256:blkSize].int_val()
        #Calculate M^3 using the chinese remainder theorem
        M3 = (((N1 * N1_inv * C1) + (N2 * N2_inv * C2) + (N3 * N3_inv * C3)) % N)

        #use given cube root function that implements binary search tree calculation to reduce runtime to O(log(n))
            #->Much faster and more reliable than pow(#, 1/3)
        M = solve_pRoot(3, M3)
        #place back into a BitVector
        cracked_bv =BitVector(intVal = M, size=256)

        #take a 128 chunk to ignore the leading zeros that were padderd
        cracked_bv_cut = cracked_bv[128:256]
        #concatenate into string and ingnore the leading null terminator
        message += cracked_bv_cut.get_bitvector_in_ascii().strip('\0')

    with open(outputF, 'w') as cracked:
        cracked.write(message)

if __name__ == '__main__':
    #python breakRSA.py -e message.txt enc1.txt enc2.txt enc3.txt n_1_2_3.txt #Steps 1 and 2
    if sys.argv[1] == '-e':
        #we need to write all the n values, and encode all of the different text files
        ''' The program should read in the plaintext file (in this case message.txt).
            – Generate the three different public and private keys, encrypts the plaintext with each of the three public keys (n1,n2,n3), and write each ciphertext to enc1.txt, enc2.txt, and enc3.txt, respectively.
            – Then the program should write each of the public keys (n1, n2, n3) to n 1 2 3.txt, with each key separated with a newline character, 
            (an example, along with their correspond- ing ciphertext, is given on the ECE404 Homework page).'''
        #generate the public keys
        public_keys, p_list, q_list = generate_p_q()
        with open(sys.argv[6], 'w') as n_file:
            for i in range(len(public_keys)):
                n_file.write(str(public_keys[i]))
                n_file.write('\n')
        #encypt the message file using all three of the public keys and store into respecive file
        encrypt(sys.argv[2], public_keys[0], p_list[0], q_list[0], sys.argv[3])
        encrypt(sys.argv[2], public_keys[1], p_list[1], q_list[1], sys.argv[4])
        encrypt(sys.argv[2], public_keys[2], p_list[2], q_list[2], sys.argv[5])
    #python breakRSA.py -c enc1.txt enc2.txt enc3.txt n_1_2_3.txt cracked.txt #Step 3
    #read n_1_2_3 file and store the values back into the list to use for decryption
    elif sys.argv[1] == '-c':
        public_keys = read_n_file(sys.argv[5])
        decrypt(public_keys, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[6])
