#HW03 Coding Problem 
#Matteo Miglio
#miglio@purdue.edu
#02/11/2021
#!/usr/bin/env python3

#mult_iv.py

import sys
'''This function was derived through the help of the following youtube video, the implementation is unique to this specific program'''
'''https://www.youtube.com/watch?v=w3m3xdw1E-Q&ab_channel=CPlus%2B'''
def multiply(x, y):
    negOrPos = False
    if ((x <  0) ^ (y < 0)):
        x, y =  abs(x), abs(y)
        negOrPos = True
    sum = 0

    while(x > 0):
        if (x & 1):
            sum = sum + y
        y = y << 1
        x = x >> 1
    if negOrPos:
        return 0-sum
    else:
        return sum

'''This function is derived from the description given in stack overflow but the implementation is my unique interpretation'''
'''https://stackoverflow.com/questions/5284898/implement-division-with-bit-wise-operator?answertab=active#tab-top'''
def divide(numerator, denominator):
    negOrPos = False
    quotient = 1
    if numerator == denominator:
        return 1
    #if the same return 1
    if ((numerator <  0) ^ (denominator < 0)):
        numerator, denominator =  abs(numerator), abs(denominator)
        negOrPos = True
    #if either of the two arguments are negative then create a true boolean, but only if one is negative HENCE XOR 
    if numerator < denominator and numerator > 0:
        return 0
    count = -1
    while denominator <= numerator:
        count = count + 1
        denominator = denominator << 1
        
    denominator = denominator >> 1
    #must run through the loop n+1 times where n is the number of shifts of the original denominator to line up the most significant 1
    for i in range(count+1):
        total = numerator - denominator
        if total >= 0:
            quotient = quotient | 1
            numerator = total
        numerator = numerator << 1
        quotient = quotient << 1
    #MUST RIGHT SHIFT TO ACCOUNT FOR PREVIOUS LEFT SHIFT
    quotient = quotient >> 1
    #IF NEG THEN RETUR 0-QUOT
    if negOrPos:
        return 0-quotient
    return quotient

if len(sys.argv) != 3:  
    sys.stderr.write("Usage: %s   <integer>   <modulus>\n" % sys.argv[0]) 
    sys.exit(1) 

NUM, MOD = int(sys.argv[1]), int(sys.argv[2])

def inv_MI(num, mod):
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = divide(num, mod)
        num, mod = mod, num % mod
        x, x_old = x_old - multiply(q, x), x
        y, y_old = y_old - multiply(q, y), y
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))

inv_MI(NUM, MOD)

