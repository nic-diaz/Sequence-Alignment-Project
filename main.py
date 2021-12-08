from time import perf_counter
import tracemalloc

filename = 'input.txt'

def generate_strings(base_strings):
    """
    Generates cumulative strings from base words and insert indicies 
    """
    strings = []
    i = 0
    j = 0

    for word in base_strings:
        cumulative_string = word

        for num in base_strings[word]:
            cumulative_string = cumulative_string[:num+1] + cumulative_string + \
                                cumulative_string[num+1:]

        strings.append(cumulative_string)
        
        # Validating the final string lengths
        k = len(base_strings[word])
        if (2**k)*len(word) != len(cumulative_string):
            print("ERROR: GENERATING FINAL STRINGS FROM INPUT FILE")
            quit()

    return strings


def parse_file(filename):
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

    base_strings = parse_file(filename)
    print(f"Generated dictionary: {base_strings}\n")

    strings = generate_strings(base_strings)
    print(f"Generated cumulative strings: {strings}\n")


    s1, s2 = strings


if __name__ == "__main__":
   main()