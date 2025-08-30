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
xl=np.int64(len(x)/10)
x=[x[i] for i in range(0,xl*10,10)]
y=np.array([data[i+2].astype(np.float64) for i in range(0,10)])
y=[[sum([y[j,i+k*10] for i in range(0,10)])*0.1 for k in range(0,xl)] for j in range(0,10)] # average for 10 elements
y0=np.array([0.0 for i in range(0,xl)]) #  y=0 line
# plotting
plt.clf()
plt.ylim(-35,10)
tl = [0] * 11
hd = []
plt.title(csvf)
for i in range(0,len(y)):
  tl[i], = plt.plot(x,y[i], label="T" + str(i),linewidth=1)
tl[10], = plt.plot(x,y0,"r",label="y=0") #  y=0 line of red
for i in range(0,len(y)+1):
  hd.append(tl[i])
  plt.legend(handles=hd,loc='upper right',bbox_to_anchor=(0.0,0.5))
ssr=data[13]
ssr=[float(ssr[i])-30.0 for i in range(0,xl*10,10)]
plt.scatter(x,ssr,marker='.',color='blue',s=1)
plt.show()