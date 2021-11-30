from collections import deque
import collections
import numpy as np

ALPHA = {('A', 'A'): 0, ('A', 'C'): 110, ('A','G'): 48, ('A', 'T'): 94,
             ('C', 'A'): 110, ('C','C'): 0, ('C','G'): 118, ('C','T'): 48,
             ('G', 'A'): 48, ('G','C'): 118, ('G','G'): 0, ('G', 'T'): 110,
             ('T', 'A'): 94, ('T','C'): 48, ('T', 'G'): 110, ('T','T'): 0}

DELTA = 30

DELTA_test = 2
ALPHA_test = {('n','m'): 1, ('a','m'): 3, ('a','e'):1, ('e','a'):1, ('m','a'):3, ('m','n'):1, ('n','e'):3, ('e','n'):3, ('m','e'):3, ('e','m'):3,('n','a'):3,('a','n'):3, ('a','a'):0, ('e','e'):0, ('m','m'):0, ('n','n'):0}

def basic(s1, s2):
    
    m = len(s1) + 1
    n = len(s2) + 1

    A = np.zeros((m, n))

    A[:, 0] = np.arange(m) * DELTA
    A[0, :] = np.arange(n) * DELTA

    for i in range(1,m):
        for j in range(1,n):
            A[i, j] = min(ALPHA[(s1[i-1], s2[j-1])] + A[i-1,j-1], DELTA + A[i-1, j], DELTA + A[i, j-1])
    return A, A[m-1,n-1]

def matchings(A, s1, s2, i, j):
    if i * j == 0 and i != j: 
        if i == 0: return [[i, j-1]] + matchings(A, s1, s2, i, j-1)
        if j == 0: return [[i-1, j]] + matchings(A, s1, s2, i-1,j)
    if i + j == 0: return []
    
    mismatch = ALPHA[(s1[i-1], s2[j-1])] + A[i-1,j-1]
    gap_up = DELTA + A[i-1, j]
    gap_left = DELTA + A[i, j-1]

    # min_idx = np.argmin([mismatch, gap_up, gap_left])
    if mismatch == A[i,j]:
        return [[i-1,j-1]] + matchings(A, s1, s2, i-1,j-1)
    elif gap_up == A[i,j]:
        return [[i-1,j]] + matchings(A, s1, s2, i-1, j)
    else:
        return [[i,j-1]] + matchings(A, s1, s2, i, j-1)

    # min_idx = np.argmin([ALPHA_test[(s1[i-1], s2[j-1])] + A[i-1,j-1], DELTA + A[i-1, j], DELTA + A[i, j-1]])
    
    if min_idx == 0:
        # print(s1[i-1], s2[j-1], (i-1,j-1))
        return [[i-1,j-1]] + matchings(A, s1, s2, i-1,j-1)
    elif min_idx == 1:
        # print(s1[i-1-1], s2[j-1], (i-1,j))
        return [[i-1,j]] + matchings(A, s1, s2, i-1, j)
    else:
        # print(s1[i-1], s2[j-1-1], (i,j-1))
        return [[i,j-1]] + matchings(A, s1, s2, i, j-1)


def alignment(s1, s2, matchings):

    final_s1 = ""
    final_s2 = ""
    for k in range(1, len(matchings)):

        x_k, y_k = matchings[k]
        x_k_minus_1, y_k_minus_1 = matchings[k-1]

        if [x+1 for x in matchings[k-1]] == matchings[k]:
            final_s1 += s1[x_k-1]
            final_s2 += s2[y_k-1]
            
        elif [x_k_minus_1+1, y_k_minus_1] == matchings[k]:
            final_s1 += s1[x_k-1]
            final_s2 += "_"
        else:
            final_s1 += "_"
            final_s2 += s2[y_k-1]

    return final_s1, final_s2

def validate(s1, s2):
    print(len(s1), len(s2))
    total_costs = 0
    for i in range(len(s1)):
        if s1[i] == "_" or s2[i] == "_":
            total_costs += DELTA 
        else:
            total_costs += ALPHA[(s1[i], s2[i])]

    return total_costs


if __name__ == "__main__":
    s1, s2 = ['ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG', 'TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG']
    s1, s2 = ['ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG','TTATTATACGCGACGCGATTATACGCGACGCG']
    s1, s2 = ['mean', 'name']
    A, opt = basic(s1, s2)
    print(A)

    opt_matching = matchings(A, s1, s2, len(s1), len(s2))
    print(opt_matching[::-1], len(opt_matching))
    print(opt)
    final_s1, final_s2 = alignment(s1, s2, opt_matching[::-1]+[[len(s1),len(s2)]])
    v = validate(final_s1, final_s2)
    print(v)
    print(final_s1)
    print(final_s2)