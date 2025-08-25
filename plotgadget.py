import csv
import sys
import numpy as np
#
data=[]
csvf=sys.argv[1]  # input file name
with open(csvf) as f:  # read csv
  reader = csv.reader(f)
  l = [row for row in reader]
  data.append(l)
#
data=data[0]
data=np.array(data)
data=data.T
x=data[1].astype(np.float64)
y=np.array([data[i+2].astype(np.float64) for i in range(0,9)])
#
  