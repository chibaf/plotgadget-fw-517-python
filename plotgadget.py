import csv
import sys
#
csvf=sys.argv[1]
with open(csvf) as f:
  reader = csv.reader(f)
  l = [row for row in reader]
#