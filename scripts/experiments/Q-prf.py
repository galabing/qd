#!/usr/bin/python

""" Each line in input file:
      tmp tmp yyyymm months precision recall

    Data will be grouped by unique 'months' field and for each group,
    a tsv file will be generated in output dir, with each line being:
      yyyymm precision recall f1
    in ascending order of yyyymm.
"""

input_dir = '/Users/lnyang/lab/qd/data/experiments/Q'
input_file = '%s/RandomForestClassifier_info' % input_dir
output_dir = '%s/misc' % input_dir

def computeF1(precision, recall):
  return 2 * precision * recall / (precision + recall)

with open(input_file, 'r') as fp:
  lines = fp.read().splitlines()
data = dict()
for line in lines[1:]:
  tmp1, tmp2, yyyymm, months, precision, recall = line.split('\t')
  months = int(months)
  if months not in data:
    data[months] = [[yyyymm, float(precision), float(recall)]]
  else:
    data[months].append([yyyymm, float(precision), float(recall)])

for months in sorted(data.keys()):
  with open('%s/months_%d_prf.tsv' % (output_dir, months), 'w') as fp:
    print >> fp, 'date\tprecisoin\trecall\tf1'
    items = sorted(data[months], key=lambda item: item[0])
    for item in items:
      yyyymm, precision, recall = item
      y = yyyymm[:4]
      m = yyyymm[4:]
      f1 = computeF1(precision, recall)
      print >> fp, '%s/%s\t%f\t%f\t%f' % (y, m, precision, recall, f1)

