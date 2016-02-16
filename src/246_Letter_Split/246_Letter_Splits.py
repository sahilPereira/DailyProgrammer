'''
Created on Dec 29, 2015

@author: Sahil
'''
import time
from _overlapped import NULL
    
num_to_alpha = { x+1: chr(ord('A')+x) for x in range(26) }
split_int = 0
output_set = list()

def getPermutations(numbers_list, start_index):
    
    i = start_index
    list_len = len(numbers_list)
    output_set.append(numbers_list)
#     print(str(numbers_list), "    Index: ",start_index)
    
    while(i < list_len):
        new_numbers_list = list(numbers_list)
        new_num = new_numbers_list[i]*10 + new_numbers_list[i+1] if i != list_len-1 else new_numbers_list[i]
        del new_numbers_list[i:i+2]
        new_numbers_list.insert(i, new_num)
        i = getPermutations(new_numbers_list, i+1)
    return start_index

def convertNumToLetter(intSet):
    
    convStr = ""
    for i in intSet:
        if i <= 0 or i >26:
            return NULL
        convStr+=num_to_alpha[i]
    return convStr

if __name__ == '__main__':

    while True:
        try:
            split_int = int(input('Enter the integer to be represented as words: '))
            break
        except ValueError:
            print('Not a valid number. Try again!')
            
    start_time = time.time()
    # Split integer into list of integers
    split_int_list = [int(i) for i in str(split_int)]
    getPermutations(split_int_list, 0)
    uniq_animal_groups = set(map(tuple, output_set))
    
    for comb in uniq_animal_groups:
        letter_split = convertNumToLetter(comb)
        if letter_split != NULL:
            print(letter_split)
            
    elapsed_time = time.time() - start_time
    print("Total time for computation and print (seconds): ",elapsed_time)
    