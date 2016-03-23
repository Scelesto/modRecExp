### LARGE INTEGER MODULAR RECURSIVE EXPONENTIATION ###
# This algorithm uses Euler's Theorem to reduce      #
# inputs, producing output orders of magnitude more  #
# efficiently than standard modular exponentiation.  #
# It is designed for large integers and will not     #
# speeed calculation for inputs less than ~25.       #
### ---------------------------------------------- ###

def modularRecursiveExponentiation(subject, exponent, modulus):
    #Recursive Mathematical Functions for Parts of the Algorithm
    def exponentiationRecursive(subject, exponent):
        if exponent is 0:
            return 1
        if exponent is 1:
            return subject
        result = exponentiationRecursive(subject, exponent >> 1)
        result *= result
        if exponent % 2 is 1:
            result *= subject
        return result
    def squareRootRecursive(value):
        def resolutionIteration(value, binaryResolution=1):
            if binaryResolution * binaryResolution < value:
                resolutionZero = resolutionIteration(value, binaryResolution << 1)
                resolutionOne = resolutionZero + binaryResolution
                if resolutionOne * resolutionOne < value:
                    return resolutionOne
                return resolutionZero
            return binaryResolution >> 1
        guess = resolutionIteration(value)
        while guess * guess <= value:
            guess += 1
        return guess
    #Find Unique Prime Factorization of Modulus
    modulusRemainder = modulus
    uniquePrimeFactorization = []
    test = 2
    squareRoot = squareRootRecursive(modulusRemainder)
    while test < squareRoot:
        if modulusRemainder % test is 0:
            uniquePrimeFactorization.append(test)
        while modulusRemainder % test is 0:
            modulusRemainder //= test
        if test > modulusRemainder:
            break
        test += 1
    if modulusRemainder >= test:
        uniquePrimeFactorization.append(modulusRemainder)
    #Assert Qualification of Modulus for Euler's Theorem Reduction
    hasDisparity = False
    for factor in uniquePrimeFactorization:
        if subject % factor is not 0:
            hasDisparity = True
            break
    #Assert Qualification of Subject for Euler's Theorem Reduction
    if hasDisparity is True:
        hasDisparity = False
        subjectRemainder = subject % modulus
        test = 2
        squareRoot = squareRootRecursive(subjectRemainder)
        while test < squareRoot:
            if subjectRemainder % test is 0 and test not in uniquePrimeFactorization:
                hasDisparity = True
                break
            while subjectRemainder % test is 0:
                subjectRemainder //= test
            if test > subjectRemainder:
                break
            test += 1
        if subjectRemainder >= test and subjectRemainder not in uniquePrimeFactorization:
            hasDisparity = True
    #If Possible, Reduce Exponent Using Euler's Theorem
    if hasDisparity is True:
        eulerPhi = modulus
        for factor in uniquePrimeFactorization:
            eulerPhi //= factor
            eulerPhi *= factor - 1
        exponent %= eulerPhi
    return exponentiationRecursive(subject % modulus, exponent) % modulus
mre = modularRecursiveExponentiation
