#!/usr/bin/env python
#!/usr/bin/env python -W ignore::DeprecationWarning

#HW04
#Matteo G. Miglio
#ECN Login: miglio@purdue.edu
#Due Date: 2/22/2021

import sys
from BitVector import *

subBytesTable = [ 99, 124, 119, 123, 242, 107, 111, 197,  48,   1, 103,  43, 254, 215, 171, 118, 202, 130, 201, 125,
                 250,  89,  71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147,  38,  54,  63, 247, 204,
                  52, 165, 229, 241, 113, 216,  49,  21,   4, 199,  35, 195,  24, 150,   5, 154,   7,  18, 128, 226,
                 235,  39, 178, 117,   9, 131,  44,  26,  27, 110,  90, 160,  82,  59, 214, 179,  41, 227,  47, 132,
                  83, 209,   0, 237,  32, 252, 177,  91, 106, 203, 190,  57,  74,  76,  88, 207, 208, 239, 170, 251,
                  67,  77,  51, 133,  69, 249,   2, 127,  80,  60, 159, 168,  81, 163,  64, 143, 146, 157,  56, 245,
                 188, 182, 218,  33,  16, 255, 243, 210, 205,  12,  19, 236,  95, 151,  68,  23, 196, 167, 126,  61,
                 100,  93,  25, 115,  96, 129,  79, 220,  34,  42, 144, 136,  70, 238, 184,  20, 222,  94,  11, 219,
                 224,  50,  58,  10,  73,   6,  36,  92, 194, 211, 172,  98, 145, 149, 228, 121, 231, 200,  55, 109,
                 141, 213,  78, 169, 108,  86, 244, 234, 101, 122, 174,   8, 186, 120,  37,  46,  28, 166, 180, 198,
                 232, 221, 116,  31,  75, 189, 139, 138, 112,  62, 181, 102,  72,   3, 246,  14,  97,  53,  87, 185,
                 134, 193,  29, 158, 225, 248, 152,  17, 105, 217, 142, 148, 155,  30, 135, 233, 206,  85,  40, 223,
                 140, 161, 137,  13, 191, 230,  66, 104,  65, 153,  45,  15, 176,  84, 187,  22]

invSubBytesTable = [ 82,   9, 106, 213,  48,  54, 165,  56, 191,  64, 163, 158, 129, 243, 215, 251, 124, 227,  57, 130,
                    155,  47, 255, 135,  52, 142,  67,  68, 196, 222, 233, 203,  84, 123, 148,  50, 166, 194,  35,  61,
                    238,  76, 149,  11,  66, 250, 195,  78,   8,  46, 161, 102,  40, 217,  36, 178, 118,  91, 162,  73,
                    109, 139, 209,  37, 114, 248, 246, 100, 134, 104, 152,  22, 212, 164,  92, 204,  93, 101, 182, 146,
                    108, 112,  72,  80, 253, 237, 185, 218,  94,  21,  70,  87, 167, 141, 157, 132, 144, 216, 171,   0,
                    140, 188, 211,  10, 247, 228,  88,   5, 184, 179,  69,   6, 208,  44,  30, 143, 202,  63,  15,   2,
                    193, 175, 189,   3,   1,  19, 138, 107,  58, 145,  17,  65,  79, 103, 220, 234, 151, 242, 207, 206,
                    240, 180, 230, 115, 150, 172, 116,  34, 231, 173,  53, 133, 226, 249,  55, 232,  28, 117, 223, 110,
                     71, 241,  26, 113,  29,  41, 197, 137, 111, 183,  98,  14, 170,  24, 190,  27, 252,  86,  62,  75,
                    198, 210, 121,  32, 154, 219, 192, 254, 120, 205,  90, 244,  31, 221, 168,  51, 136,   7, 199,  49,
                    177,  18,  16,  89,  39, 128, 236,  95,  96,  81, 127, 169,  25, 181,  74,  13,  45, 229, 122, 159,
                    147, 201, 156, 239, 160, 224,  59,  77, 174,  42, 245, 176, 200, 235, 187,  60, 131,  83, 153,  97,
                     23,  43,   4, 126, 186, 119, 214,  38, 225, 105,  20,  99,  85,  33,  12, 125]

AES_modulus = BitVector(bitstring='100011011')

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

def g(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = g(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8]
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

def gen_round_keys(keyText):
    key_words = []
    key_bv = BitVector( textstring = keyText)
    key_words = gen_key_schedule_256(key_bv)

    key_schedule = []
    for word_index,word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i*8:i*8+8].intValue())
        if word_index % 4 == 0: print("\n")
        key_schedule.append(keyword_in_ints)
    num_rounds = 14

    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])
    print("\n\nRound keys in hex (first key for input block):\n")
    #for round_key in round_keys:
    #    print(round_key)
    #print()
    return round_keys

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

def shift_rows(state_array):
    '''
    Obtained from StackOverFlow https://stackoverflow.com/questions/2150108/efficient-way-to-rotate-a-list-in-python
    this function will: 
    #FIRST YOU MUST CHANGE INTO LITERAL HEX VALUES OR ELSE THE LIST WILL MESS WITH THE ADDRESSES OF THE BITVECTOR POINTERS
    1.shift the top row of the state array no spots
    2. Shift the second row of the state array by 1 index circularly to the left
    3. Shift the third row of the state array by 2 indicies circularly to the left
    4. Shift the fourth row of the state array by 3 indicies circularly to the left
    '''
    for i in range(4):
        for j in range(4):
            state_array[i][j] = hex(state_array[i][j].int_val())

    for r in range(1, 4):
        state_array[r] = state_array[r][r:] + state_array[r][:r]
    return state_array

def invShift_rows(state_array):
    '''
    Obtained from StackOverFlow https://stackoverflow.com/questions/2150108/efficient-way-to-rotate-a-list-in-python
    this function will: 
    1.shift the top row of the state array no spots
    2. Shift the second row of the state array by 1 index circularly to the left
    3. Shift the third row of the state array by 2 indicies circularly to the left
    4. Shift the fourth row of the state array by 3 indicies circularly to the left
    '''
    for r  in range(1, 4):
        state_array[r] = state_array[r][-r:] + state_array[r][:-r]
    return state_array
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=# 
'''
1. Create a temp vector that will be used to return the hex version of the byteSubstituted array
2. temp_state used to copy state (state is hex) into BitVector and pad it for bits
3. Need BitVector to split into left and right halves to index into the 0-255 for subBytes
4. Index into table and return both state array and hex version
'''
def byteSubstitution(state_array):
    temp_state_array = [[BitVector(size=8) for _ in range(4)] for _ in range(4)]
    temp = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            temp_state_array[i][j] = BitVector(intVal=int(state_array[i][j], 16))
            if len(temp_state_array[i][j]) < 8:
                temp_state_array[i][j].pad_from_left(8-len(temp_state_array[i][j]))

    for i in range(4):
        for j in range(4):
            if(len(temp_state_array[i][j]) != 8):
               temp_state_array[i][j].pad_from_left(8-len(temp_state_array[i][j]) % 8)
            [left, right] = (temp_state_array[i][j].divide_into_two())
            row, column = int(str(left), 2), int(str(right), 2)
            index = (16 * row) + column

            temp_state_array[i][j] = BitVector(intVal = int(subBytesTable[index]))

    for i in range(4):
        for j in range(4):
            temp[i][j] = hex(temp_state_array[i][j].int_val())
    return temp_state_array, temp

def invByteSubstitution(state_array):
    temp_state_array = [[BitVector(size=8) for _ in range(4)] for _ in range(4)]
    temp = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            temp_state_array[i][j] = BitVector(intVal=int(state_array[i][j], 16))
            if len(temp_state_array[i][j]) < 8:
                temp_state_array[i][j].pad_from_left(8-len(temp_state_array[i][j]))

    for i in range(4):
        for j in range(4):
            if(len(temp_state_array[i][j]) != 8):
               temp_state_array[i][j].pad_from_left(8-len(temp_state_array[i][j]) % 8)
            [left, right] = (temp_state_array[i][j].divide_into_two())
            row, column = int(str(left), 2), int(str(right), 2)
            index = (16 * row) + column

            temp_state_array[i][j] = BitVector(intVal = int(invSubBytesTable[index]))

    for i in range(4):
        for j in range(4):
            temp[i][j] = hex(temp_state_array[i][j].int_val())
    return temp_state_array, temp
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=Inverse Mixing of the Columns-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=# 

def inverse_mix_columns(state_array):
    '''
        You MUST CREATE A DEEP COPY OF THE STATE_ARRAY TO AVOID USING REPEAT/ALTERED VALUES IN THE OLD STATE ARRAY
        CREDIT GIVEN: AMAN PATEL 
    '''
    temp_state_array = [[BitVector(size=8) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            state_array[i][j] = BitVector(intVal=int(state_array[i][j], 16))
            if len(temp_state_array[i][j]) < 8:
                state_array[i][j].pad_from_left(8-len(state_array[i][j]) % 8)
            temp_state_array[i][j] = state_array[i][j].deep_copy()
    hex09 = BitVector(hexstring = '09') 
    hex0B = BitVector(hexstring = '0b')
    hex0D = BitVector(hexstring = '0d') 
    hex0E = BitVector(hexstring = '0e')
    #create a blank state array that needs to be a BitVector in order to carry out modulus multiplications
    #state_array = [[BitVector(size = 8) for _ in range(4)] for _ in range(4)]

    
    for i in range(0,4):
        state_array[0][i] = temp_state_array[0][i].gf_multiply_modular(hex0E, AES_modulus, 8) ^ temp_state_array[1][i].gf_multiply_modular(hex0B, AES_modulus, 8) ^ temp_state_array[2][i].gf_multiply_modular(hex0D, AES_modulus, 8) ^ temp_state_array[3][i].gf_multiply_modular(hex09, AES_modulus, 8)
        
        state_array[1][i] = temp_state_array[0][i].gf_multiply_modular(hex09, AES_modulus, 8) ^ temp_state_array[1][i].gf_multiply_modular(hex0E, AES_modulus, 8) ^ temp_state_array[2][i].gf_multiply_modular(hex0B, AES_modulus, 8) ^ temp_state_array[3][i].gf_multiply_modular(hex0D, AES_modulus, 8)
        
        state_array[2][i] = temp_state_array[0][i].gf_multiply_modular(hex0D, AES_modulus, 8) ^ temp_state_array[1][i].gf_multiply_modular(hex09, AES_modulus, 8) ^ temp_state_array[2][i].gf_multiply_modular(hex0E, AES_modulus, 8) ^ temp_state_array[3][i].gf_multiply_modular(hex0B, AES_modulus, 8)
        
        state_array[3][i] = temp_state_array[0][i].gf_multiply_modular(hex0B, AES_modulus, 8) ^ temp_state_array[1][i].gf_multiply_modular(hex0D, AES_modulus, 8) ^ temp_state_array[2][i].gf_multiply_modular(hex09, AES_modulus, 8) ^ temp_state_array[3][i].gf_multiply_modular(hex0E, AES_modulus, 8)
    
    for i in range(4):
        for j in range(4):
            state_array[i][j] = hex(state_array[i][j].int_val())
    
    return state_array

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=# 

def mix_columns(state_array):
    '''
        You MUST CREATE A DEEP COPY OF THE STATE_ARRAY TO AVOID USING REPEAT/ALTERED VALUES IN THE OLD STATE ARRAY
        CREDIT GIVEN: AMAN PATEL 
    '''

    temp_state_array = [[BitVector(size=8) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            state_array[i][j] = BitVector(intVal=int(state_array[i][j], 16))
            if len(temp_state_array[i][j]) < 8:
                state_array[i][j].pad_from_left(8-len(state_array[i][j]) % 8)
            temp_state_array[i][j] = state_array[i][j].deep_copy()

    hex02 = BitVector(bitstring = '00000010') 
    hex03 = BitVector(bitstring = '00000011')
    #create a blank state array that needs to be a BitVector in order to carry out modulus multiplications
    #state_array = [[BitVector(size = 8) for _ in range(4)] for _ in range(4)]

    
    for i in range(0,4):
        state_array[0][i] = (temp_state_array[0][i].gf_multiply_modular(hex02, AES_modulus, 8)) ^ (temp_state_array[1][i].gf_multiply_modular(hex03, AES_modulus, 8)) ^ (temp_state_array[2][i]) ^ (temp_state_array[3][i])

        state_array[1][i] = (temp_state_array[0][i]) ^ (temp_state_array[1][i].gf_multiply_modular(hex02, AES_modulus, 8)) ^ (temp_state_array[2][i].gf_multiply_modular(hex03, AES_modulus, 8)) ^ (temp_state_array[3][i])

        state_array[2][i] = (temp_state_array[0][i]) ^ (temp_state_array[1][i]) ^ (temp_state_array[2][i].gf_multiply_modular(hex02, AES_modulus, 8)) ^ (temp_state_array[3][i].gf_multiply_modular(hex03, AES_modulus, 8))

        state_array[3][i] = (temp_state_array[0][i].gf_multiply_modular(hex03, AES_modulus, 8)) ^ (temp_state_array[1][i]) ^ (temp_state_array[2][i])  ^ (temp_state_array[3][i].gf_multiply_modular(hex02, AES_modulus, 8))
    
    '''CHANGE  BACK INTO HEX VALUE'''
    for i in range(4):
        for j in range(4):
            state_array[i][j] = hex(state_array[i][j].int_val())
    
    return state_array

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

def state_array_to_hexBlock(state_array):
    """
    This is adapted from Brian Rieder https://github.com/brian-rieder/computer-security/blob/58ba8721aea00e5a376ebcc5080ea39e504de80b/AES/aes.py#L100
    1. Changes State array into form of word block, the same way it is read in from the file as one big hex string
    2. In order to XOR with roundKey[round]
    """
    temp_bv = BitVector(intVal=int(str(state_array[0][0]), 16))
    if len(temp_bv) < 8:
        temp_bv.pad_from_left(8 - len(temp_bv) % 8)
    bv = temp_bv
    for j in range(4):
        for i in range(4):
            if i != 0 or j != 0:
                temp_bv = BitVector(intVal=int(str(state_array[i][j]), 16))
                if len(temp_bv) < 8:
                    temp_bv.pad_from_left(8-(len(temp_bv)))
                bv += temp_bv
    return bv

def AES_encrypt():
    file_out = open(sys.argv[4], "w")
    with open(sys.argv[3], 'r') as keyFile:
        key_plaintext = keyFile.read()

    key_bv = BitVector(textstring=key_plaintext)
    input_bv = BitVector(filename=sys.argv[2])
    round_keys = gen_round_keys(key_plaintext)

    #state array needs to be a 4x8 array where the next element in the array is down in the column not across in the row
    #needs to be 4x8 because we have a key size of 256/8 words = [(4 bytes) * (8 bits per byte) * (8 columns)]

    input_state_array = [[0 for _ in range(4)] for _ in range(4)]
    output_state_array = [[0 for _ in range(4)] for _ in range(4)]

    while (input_bv.more_to_read):
        text_block = input_bv.read_bits_from_file(128)
        if text_block.length() != 128:
            text_block.pad_from_right(128 - text_block.length() % 128)

        #adding initial round key to the block, then going from 1-14 rounds for 256 key size. 
        text_block ^= round_keys[0]
        #code given in lecture to break up 128 bit sized block into list of lists
        for i in range(4):
            for j in range(4):
                output_state_array[j][i] = hex(text_block[32*i + 8*j:32*i + 8*(j+1)].int_val())
                
        for round in range(1, 14):
            #we need to have an extra array, as state_array is constantly  switching between BitVector and hex, so it is easy to maintain
            #ooutput as a blank hex array that can easily be updated after XORing with roundKey which produces a hex block
            input_state_array = output_state_array
            input_state_array, printTest = byteSubstitution(input_state_array)
            #shift rows needs a hex argument no BitVector or else it
            input_state_array = shift_rows(input_state_array)

            input_state_array = mix_columns(input_state_array)
            #must change the state_array to one long bitvector like the input word plaintext block so we are able to XOR it with the round key
            input_state_array = round_keys[round] ^ state_array_to_hexBlock(input_state_array)

            #NEED it back into hex block formn for the rest of the encryption rounds 
            for i in range(4):
                for j in range(4):
                    output_state_array[j][i] = hex(input_state_array[32*i + 8*j:32*i + 8*(j+1)].int_val())

        input_state_array, printTest = byteSubstitution(output_state_array)

        input_state_array = shift_rows(input_state_array)

        input_state_array = round_keys[14] ^ state_array_to_hexBlock(input_state_array)

        hex_block = input_state_array.get_bitvector_in_hex()
        file_out.write(hex_block)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

def AES_decrypt():
    file_out = open(sys.argv[4], "w")
    with open(sys.argv[3], 'r') as keyFile:
        key_plaintext = keyFile.read()
    with open(sys.argv[2]) as IP:
        input_bv = BitVector(hexstring = IP.read())

    encryptedFileLen = len(input_bv)

    key_bv = BitVector(textstring=key_plaintext)
    round_keys = gen_round_keys(key_plaintext)

    input_state_array = [[0 for _ in range(4)] for _ in range(4)]
    output_state_array = [[0 for _ in range(4)] for _ in range(4)]

    strg = ""
    for blkSize in range(128, encryptedFileLen+1, 128):
        bitvec = input_bv[blkSize-128:blkSize]
        #adding initial round key to the block, then going from 1-14 rounds for 256 key size. 
        bitvec ^= round_keys[14]
        for i in range(4):
            for j in range(4):
                output_state_array[j][i] = hex(bitvec[32*i + 8*j:32*i + 8*(j+1)].int_val())
        for round in range(13, 0, -1):
            input_state_array = output_state_array
            #already in hex so we can just send to shift rows
            input_state_array = invShift_rows(input_state_array)
            #convert to bitvector  in the function so we can split for indexing
            input_state_array, printTest = invByteSubstitution(input_state_array)
            #use printTest because that is the hex form of the state_array which will be sent to state_array_to_hexblock -> arg needs to be ~Bitvector[][]
            input_state_array = round_keys[round] ^ state_array_to_hexBlock(printTest)

            for i in range(4):
                for j in range(4):
                    output_state_array[j][i] = hex(input_state_array[32*i + 8*j:32*i + 8*(j+1)].int_val())

            input_state_array = inverse_mix_columns(output_state_array)

        output_state_array = invShift_rows(output_state_array)

        input_state_array, printTest = invByteSubstitution(output_state_array)

        input_state_array = round_keys[0] ^ state_array_to_hexBlock(printTest)

        if input_state_array.length() != 128:
            input_state_array.pad_from_right(128 - input_state_array.length() % 128)

        strg += input_state_array.get_bitvector_in_ascii()

    file_out.write(strg)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

if __name__ == '__main__':
    if sys.argv[1] == "-e":
        AES_encrypt()
    else:
        AES_decrypt()