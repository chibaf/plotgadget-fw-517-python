import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
#
data=[]
csvf=sys.argv[1]  # input file name
with open(csvf) as f:  # read csv
  reader = csv.reader(f)
  l = [row for row in reader]
  data.append(l)
#
data=data[0]  # data conversion
data=np.array(data)
data=data.T  # transpose
x=data[1].astype(np.float64)
y=np.array([data[i+2].astype(np.float64) for i in range(0,10)])
# plotting
plt.clf()
plt.ylim(-20,20)
tl = [0] * 10
hd = []
for i in range(0,len(y)):
  tl[i], = plt.plot(x,y[i], label="T" + str(i+1))
for i in range(0,len(y)):
  hd.append(tl[i])
  plt.legend(handles=hd)
plt.show()