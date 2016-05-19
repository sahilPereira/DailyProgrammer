'''
Created on Mar 20, 2016

@author: Sahil
'''

def guessHat(isPrevOdd, remainingHats):
    
    while len(remainingHats) != 0:
        if len(remainingHats) == 1:
            guessedHats.append("Black" if isPrevOdd else "White")
            return
        
        isNewOdd = isOddBlackHats(remainingHats[1:])
        # this person will have white hat
        if isPrevOdd == isNewOdd:
            guessedHats.append("White")
        else:
            guessedHats.append("Black")
            isPrevOdd = not isPrevOdd
        remainingHats = remainingHats[1:]
    return

def isOddBlackHats(hats_in_front):
    isOdd = False
    for hat in hats_in_front:
        if hat.strip() == 'Black':
            isOdd = not isOdd
    return isOdd

guessedHats = []
if __name__ == '__main__':
    
    with open('largeListOfHats') as f:
        lines = f.readlines()
    input_list = lines[0:]
    
    # first guess
    guess = isOddBlackHats(input_list[1:])
    guessHat(guess, input_list)
    
    for idx, guess in enumerate(guessedHats):
        if guess == input_list[idx].strip():
            print("Correct:    Actual=%s    |    Guess=%s"% (input_list[idx].strip(), guess))
        else:
            print("Incorrect:    Actual=%s    |    Guess=%s"% (input_list[idx].strip(), guess))
    
    
    