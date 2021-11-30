import numpy as np
from basic import basic, matchings, alignment, validate
# from sequence_alignment1 import alignment
filename = "BaseTestcases_CS570FinalProject/input1.txt"

def generate_strings(base_strings):
    """
    Generates cumulative strings from base words and insert indicies 
    """
    strings = []

    for word in base_strings:
        cumulative_string = word

        for num in base_strings[word]:
            cumulative_string = cumulative_string[:num+1] + cumulative_string + \
                                cumulative_string[num+1:]

        strings.append(cumulative_string)

    return strings


def parse_file():
    """
    Returns a dictionary with base strings and indicies for cumulative string creation
    For example: {'ACTG': [3, 6, 1, 1], 'TACG': [1, 2, 9, 2]} 
    """
    base_strings = {}
    base_str = ''
    
    with open(filename) as file:
        for line in file:
            line = line.rstrip()

            if line.isdigit() == True:
                base_strings[base_str].append(int(line))
            else:
                base_strings[line] = [] 
                base_str = line
    
    return base_strings

def main():

    base_strings = parse_file()
    print(f"Generated dictionary: {base_strings}\n")

    strings = generate_strings(base_strings)
    print(f"Generated cumulative strings: {strings}\n")

    s1, s2 = strings
    print(strings)
    # s = alignment(s1, s2) Adrianne's
    # print(s)
    A, opt = basic(s1, s2)

    opt_matching = matchings(A, s1, s2, len(s1), len(s2))
    final_s1, final_s2 = alignment(s1, s2, opt_matching[::-1]+[[len(s1),len(s2)]])

    print(opt_matching[::-1]+[[len(s1),len(s2)]], opt)
    print(f"validated_costs: {validate(final_s1, final_s2)}") # correct cost but not the same output1

    print(final_s1[:50], final_s1[-50:])
    print(final_s2[:50], final_s2[-50:])

if __name__ == "__main__":
   main()