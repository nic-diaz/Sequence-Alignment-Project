from random import randrange
import numpy as np
import matplotlib.pyplot as plt
from main import generate_strings
from basic import basic, validate, find_solution
from efficient import efficient
import itertools

def generate_base_strings(letters, MAX_INPUT_LEN, MAX_FINAL_STR_LEN):
    """
    Returns a RANDOM dictionary with base strings and indicies for cumulative string creation
    For example:{'TGTA': [3, 5, 3, 1, 13, 17, 12], 'GCGGGTGC': [3, 6, 19]}
    """
    s1_len = randrange(1, MAX_INPUT_LEN + 1)
    s2_len = randrange(1, MAX_INPUT_LEN + 1)
    
    s1 = ''
    s2 = ''
    
    for index in range(s1_len):
        rand_indx = randrange(len(letters))
        s1 += letters[rand_indx]
        
    for index in range(s2_len):
        rand_indx = randrange(len(letters))
        s2 += letters[rand_indx]
    
    s1_list_length = randrange(MAX_FINAL_STR_LEN + 1)
    s2_list_length = randrange(MAX_FINAL_STR_LEN + 1)
    s1_list = []
    s2_list = []
    #print(f's1: {s1}, s2: {s2}')
    
    for index in range(s1_list_length):
        insert_index = randrange((index+1)*s1_len)
        s1_list.append(insert_index)
        
    for index in range(s2_list_length):
        insert_index = randrange((index+1)*s2_len)
        s2_list.append(insert_index)
    
    base_strings = {}
    
    base_strings[s1] = s1_list
    base_strings[s2] = s2_list
        
    return base_strings

def test_strings(s1, s2, base_strings, verbose=0):
    '''
    Computes optimal cost from 2 final strings for basic and efficient versions. 
    Verbose for debug printout
    '''
    
    if (verbose):
        print(f'Testing {base_strings}')
    
    _, _, opt_basic = basic(s1, s2)
    
    alignments = efficient(s1, s2)
    alignments.sort()
    alignments = list(k for k,_ in itertools.groupby(alignments))
    final_s1, final_s2 = find_solution(s1, s2, alignments)
    opt_efficient = validate(final_s1, final_s2)
    
    if (verbose):
        if opt_basic != opt_efficient:
            print(f'FAILED. basic: {opt_basic}, efficient: {opt_efficient}')
        else:
            print(f'PASSED. basic: {opt_basic}, efficient: {opt_efficient}')
    
    return 0    
    
    
def main():
    letters = ['A', 'C', 'T', 'G']
    MAX_INPUT_LEN = 10 # Max length of string in the input.txt file (before string generation)
    MAX_FINAL_STR_LEN = 10 # Max length of final (genereated) string 2**10  
    NUM_TESTCASES = 20 # Number of tests to run
    
    base_strings = {}
    
    for index in range(NUM_TESTCASES):
        base_strings = generate_base_strings(letters, MAX_INPUT_LEN, MAX_FINAL_STR_LEN)
        
        #print(f'base strings: {base_strings}')
        strings = generate_strings(base_strings)
        s1, s2 = strings
        
        #print(f's1: {s1}, s2: {s2}')
        
        test_strings(s1, s2, base_strings, 1)
            
if __name__ == "__main__":
   main()
