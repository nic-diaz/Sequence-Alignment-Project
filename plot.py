import os
from matplotlib import pyplot as plt
from tqdm import tqdm
from time import perf_counter

def plot(f, x,y1, y2):
  plt.plot(x,y1, label="basic")
  plt.plot(x,y2, label=f"efficient")

  plt.xlabel('m+n')
  plt.xticks(rotation=45)
  ylabel = 'time (s)' if f == "time" else 'memory (kB)'
  plt.ylabel(ylabel)

  plt.legend()
  filename = 'CPUPlot.png' if f == "time" else "MemoryPlot.png"
  plt.savefig(filename, bbox_inches='tight')
  plt.close()

def extract_info():
  bxs, exs, btimes, etimes, bmems, emems = [], [], [], [], [], []

  with open('test.txt', 'r') as fr:
    for line in fr:
      alg, mn, t, m = line.rstrip().split(',')

      if alg == "basic":
        bxs.append(int(mn))
        btimes.append(round(float(t),2))
        bmems.append(float(m))

      else:
        exs.append(int(mn))
        etimes.append(round(float(t),2))
        emems.append(float(m))
  
  bxs, btimes, bmems = zip(*sorted(zip(bxs, btimes, bmems)))
  exs, etimes, emems = zip(*sorted(zip(exs, etimes, emems)))

  plot("time", bxs, btimes, etimes)
  plot("memory", exs, bmems, emems)

if __name__ == "__main__":
  start = perf_counter()

  for f in tqdm(os.listdir('./Testing')):
    print("\n",f)
    os.system(f'python3 basic_1083157262_9819019274_9267915615.py Testing/{f}')
    os.system(f'python3 efficient_1083157262_9819019274_9267915615.py Testing/{f}')

  print(perf_counter()-start)
  extract_info()
