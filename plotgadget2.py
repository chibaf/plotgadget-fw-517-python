def cm(x):
  if x==1:
    return "r"
  else:
    return "k"

import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
#
data=[]
# input file name
csvf=sys.argv[1]  
with open(csvf) as f:  # read csv
  reader = csv.reader(f)
  l = [row for row in reader]
  data.append(l)
# data conversion
data=data[0]  
data=np.array(data)
data=data.T  # transpose
x=data[1].astype(np.float64)
y=np.array([data[i+2].astype(np.float64) for i in range(0,10)])
colors=[cm(data[13][i]) for i in range(0,len(data[13]))]
colors=np.array(colors)
y0=np.array([0.0 for i in range(0,len(x))]) #  y=0 line
y1=np.array([-15.0 for i in range(0,len(x))]) #  y=-15 line
# plotting
plt.clf()
plt.ylim(-20,20)
tl = [0] * 11
hd = []
tl[0], = plt.plot(x,y0,"r",label="y=0") #  y=0 line of red
plt.scatter(x, y1, s=0.1, c=colors)
for i in range(0,len(y)):
  tl[i+1], = plt.plot(x,y[i], label="T" + str(i+1))
for i in range(0,len(y)+1):
  hd.append(tl[i])
  plt.legend(handles=hd)
plt.show()