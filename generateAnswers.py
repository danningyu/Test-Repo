class FloatingPoint:
    origValue = None
    sign = None
    exponent = None
    mantissa = None

    def outputToFile(self):
        return format(self.origValue, '013b') + "\n" + format(self.sign, '01b') + "\n" + format(self.exponent, '03b') + "\n" + format(self.mantissa, '05b') + '\n'

    def __str__(self):
        twosComp = None
        if self.origValue > 4095:
            twosComp = -8192 + self.origValue
        else:
            twosComp = self.origValue
        return format(twosComp, 'd') + "," + format(self.origValue, '013b') + "," + format(self.sign, '01b') + "," + format(self.exponent, '03b') + "," + format(self.mantissa, '05b')

def convertNumber(number):
    result = FloatingPoint()
    result.origValue = number
    if number & 0b1000000000000: #"negative"
        result.sign = 1
        number = 8192 - number
    else:
        result.sign = 0
        if number > 3968:
            result.exponent = 7
            result.mantissa = 31
            return result    
    
    exponentTemp = 0
    mantissaTemp = 0

    if (number >> 12) & 0b1:
        exponentTemp = 7
    elif (number>>11) & 0b1:
        exponentTemp = 7
    elif (number>>10) & 0b1:
        exponentTemp = 6
    elif (number>>9) & 0b1:
        exponentTemp = 5
    elif (number>>8) & 0b1:
        exponentTemp = 4
    elif (number>>7) & 0b1:
        exponentTemp = 3
    elif (number>>6) & 0b1:
        exponentTemp = 2
    elif (number>>5) & 0b1:
        exponentTemp = 1
    else:
        exponentTemp = 0

    mantissaTemp = (number >> exponentTemp) & 0b11111
    if number == 4096:
        mantissaTemp = 31
        exponentTemp = 7
    
    sixthBit = None

    if exponentTemp == 0:
        sixthBit = 0    
    else:
        sixthBit = (number >> (exponentTemp-1)) & 0b1
    
    if sixthBit and mantissaTemp == 31 and exponentTemp != 7:
        #case where it overflows, so (31+1)/2 = 16, exp + 1
        #but only do this if exp isn't already max
        exponentTemp += 1
        mantissaTemp = 0b10000
    elif sixthBit and mantissaTemp < 31:
        #we need to round, but only when it won't oveflow
        mantissaTemp += 1
    
    result.exponent = exponentTemp
    result.mantissa = mantissaTemp
    return result

def convertAllNumbers():
    result = None
    START_NUM = 0
    END_NUM = 8191
    f = open('../Project2/progConversion.txt', 'w')
    for i in range(START_NUM, END_NUM+1):
        result = convertNumber(i)
        f.write(result.outputToFile())
        if i == 0 or i == 1 or i == 3967 or i == 3840 or i == 3968 or i == 3969 or i == 4095 or i == 4096 or i == 4097 or i == 8190 or i == 8191:
            print(result)
    f.close()

if __name__ == "__main__":
    convertAllNumbers()