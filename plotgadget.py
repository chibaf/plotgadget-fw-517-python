import csv
import sys
import numpy as np
#
csvf=sys.argv[1]
with open(csvf) as f:
  reader = csv.reader(f)
  l = np.array([row for row in reader])
#
  l2=l.T
  m=np.array([l2[i+1] for i in range(0,11)])
  x=m.astype(np.float64)
  print(x[0])
  