#!/usr/bin/python

""" Calculates distribution of data for training/testing.
    month => count(data)
"""

meta_file = '/Users/lnyang/lab/qd/data/experiments/Q/all/meta'
distr_file = '/Users/lnyang/lab/qd/data/experiments/Q/all/distr.tsv'

with open(meta_file, 'r') as fp:
  lines = fp.read().splitlines()
stats = dict()
for line in lines:
  ticker, date, tmp1, tmp2 = line.split('\t')
  y, m, d = date.split('-')
  ym = '%s-%s' % (y, m)
  if ym not in stats:
    stats[ym] = 1
  else:
    stats[ym] += 1

with open(distr_file, 'w') as fp:
  for ym in sorted(stats.keys()):
    count = stats[ym]
    print >> fp, '%s\t%d' % (ym, count)

