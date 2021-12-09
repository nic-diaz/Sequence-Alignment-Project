from basic import basic, alignment, find_solution, validate
import sys
import numpy as np
from main import parse_file
from main import generate_strings
import matplotlib.pyplot as plt
import itertools
from time import perf_counter
import tracemalloc


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


def plot_P(P):
  # plot
  x = []
  y = []
  for item in P:
    x.append(item[0])
    y.append(item[1])
  
  fig, ax = plt.subplots()
  plt.scatter(x, y)
  major_ticks = np.arange(0, 64, 10)
  minor_ticks = np.arange(0, 64, 1)
  ax.set_xticks(major_ticks)
  ax.set_xticks(minor_ticks, minor=True)
  ax.set_yticks(major_ticks)
  ax.set_yticks(minor_ticks, minor=True)
  ax.grid(which='both')
  
def efficient(s1, s2, s1_offset=0, s2_offset=0):
  m = len(s1)
  n = len(s2)

  if m <= 2 or n <= 2:
    _,opt_alignment, _ = basic(s1, s2)
    P.extend([[p1+s1_offset, p2 + s2_offset] for p1,p2 in opt_alignment])
    return P
  
  F = space_efficient_alignment(s1, s2[:n//2])
  G = space_efficient_alignment(s1[::-1], s2[n//2:][::-1])

  # F,_,_ = basic(s1, s2[:n//2])
  # G,_,_ = basic(s1[::-1], s2[n//2:][::-1])

  q_val = 100000000000
  q = 0

  for i in range(len(F)):
    opt_q = F[i] + G[m-i]
    if opt_q < q_val:
      q_val = opt_q
      q = i

  P.append([s1_offset+q, s2_offset+(n//2)])

  # plot_P(P)
  # plt.show()
  efficient(s1[:q], s2[:n//2], s1_offset, s2_offset)
  
  s1_offset += q
  s2_offset += (n//2)

  efficient(s1[q:], s2[(n//2):], s1_offset, s2_offset)
  
  return P

if __name__ == "__main__":
  
  base_strings = parse_file(filename)
  strings = generate_strings(base_strings)
  s1, s2 = strings
  
  tracemalloc.start()
  start = perf_counter()
  alignments = efficient(s1, s2)
  end = perf_counter()
  
  alignments.sort()
  alignments = list(k for k,_ in itertools.groupby(alignments))
  
  final_s1, final_s2 = find_solution(s1, s2, alignments)
  opt = validate(final_s1, final_s2)


  with open('output.txt','w') as f:
    f.write(final_s1[:50] + " " + final_s1[-50:] + "\n")
    f.write(final_s2[:50] + " " + final_s2[-50:] + "\n")
    f.write(str(opt) + "\n")
    f.write(str(end-start) + "\n")
    f.write(str(tracemalloc.get_traced_memory()))
    
    
  #print(validate(final_s1, final_s2)) # alignment cost value
  '''
  print(f'Efficient: {alignments}\n')
  final_s1, final_s2 = find_solution(s1, s2, alignments)
  print(final_s1)
  print(final_s2)
  print(validate(final_s1, final_s2)) # alignment cost value
  '''