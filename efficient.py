from basic import basic, alignment, find_solution, validate
import numpy as np

ALPHA =     {('A', 'A'): 0, ('A', 'C'): 110, ('A','G'): 48, ('A', 'T'): 94,
             ('C', 'A'): 110, ('C','C'): 0, ('C','G'): 118, ('C','T'): 48,
             ('G', 'A'): 48, ('G','C'): 118, ('G','G'): 0, ('G', 'T'): 110,
             ('T', 'A'): 94, ('T','C'): 48, ('T', 'G'): 110, ('T','T'): 0}

DELTA = 30

P = []

def space_efficient_alignment(s1,s2):
  m = len(s1) + 1
  n = len(s2) + 1

  B = np.zeros((m, 2))

  B[:, 0] = np.arange(m) * DELTA

  for j in range(1,n):
    B[0,1] = j * DELTA

    for i in range(1,m):
        B[i, 1] = min(ALPHA[(s1[i-1], s2[j-1])] + B[i-1,0], DELTA + B[i-1, 1], DELTA + B[i, 0])

    B[:,0] = B[:,1]

  return B[:,1]

def backward_space_efficient_alignment(s1,s2):
  m = len(s1) + 1
  n = len(s2) + 1

  B = np.zeros((m, 2))

  B[:, 1] = np.arange(m-1,-1,-1) * DELTA

  for j in range(n-2,-1,-1):
    print(j, n, n- j-2)
    B[m-1,0] = n-j-2 * DELTA

    # for i in range(1,m):
    #   bm = m - 1 - i
    #   B[bm, 0] = min(ALPHA[(s1[i-1], s2[j-1])] + B[bm+1,1], DELTA + B[bm+1, 0], DELTA + B[bm, 1])

    for i in range(m-2,-1,-1):
      # print(i, len(s1), len(s2))
      B[i, 0] = min(ALPHA[(s1[i], s2[j])] + B[i+1,1], DELTA + B[i+1, 0], DELTA + B[i, 1])
    
  
    B[:,1] = B[:,0]

  return B[:,0]

def efficient(s1, s2):
  m = len(s1)
  n = len(s2)

  if m <= 2 or n <= 2:
    opt_alignment, _, _, _ = basic(s1, s2)
    print(opt_alignment)
    P.extend(opt_alignment)
    return None
  
  F = space_efficient_alignment(s1, s2[:n//2])
  G = space_efficient_alignment(s1[::-1], s2[n//2:][::-1])

  q_val = 100000000000
  q = 0
  print('len',len(F), len(G))
  # print(F)
  # print(G)
  for i in range(len(F)):
    opt_q = F[i] + G[i]
    # print([opt_q, q_val])
    if np.argmin([opt_q, q_val]) == 0:
      q_val = opt_q
      q = i

  # print(q)
  P.append([q, n // 2])

  efficient(s1[:q], s2[:n//2])
  efficient(s1[q:], s2[n//2:])

  return P

if __name__ == "__main__":
  s1, s2 = ['ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG', 'TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG']
  # s1, s2 = ['ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG','TTATTATACGCGACGCGATTATACGCGACGCG']
  # opts = space_efficient_alignment(s1, s2)
  # optbs = space_efficient_alignment(s1[::-1], s2[::-1])
  # # optbs = backward_space_efficient_alignment(s1, s2)
  # print(opts)
  # print(optbs)
  alignments = efficient(s1, s2)
  print(len(s1),len(s2))
  print(alignments)
  final_s1, final_s2 = find_solution(s1, s2, alignments[::-1])
  print(final_s1)
  print(final_s2)
  print(validate(final_s1, final_s2))
