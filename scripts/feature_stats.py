#!/usr/bin/python

import os

feature_dir = '/Users/lnyang/lab/qd/data/features'
excluded = set(['pegain', 'pgain', 'misc'])
stats_file = '%s/misc/stats.tsv' % feature_dir

info_header = '\t'.join(
    ['year', 'count', 'total', 'coverage', 'avg', 'min', '1perc', '10perc',
     '25perc', '50perc', '75perc', '90perc', '99perc', 'max'])

headers = ['feature\\stats', 'coverage', '1perc', '99perc']
stats_index = {  # must be consistent with headers
    'coverage': 1,
    '1perc': 2,
    '99perc': 5,
}

features = sorted([feature for feature in os.listdir(feature_dir)
                   if feature not in excluded])
print 'processing %d features' % len(features)

with open(stats_file, 'w') as fp:
  print >> fp, '\t'.join(headers)
  for feature in features:
    info_file = '%s/%s/info' % (feature_dir, feature)
    with open(info_file, 'r') as ifp:
      lines = ifp.read().splitlines()
    assert len(lines) > 2
    assert lines[1] == info_header
    coverages = []
    perc1s = []
    perc99s = []
    for i in range(2, len(lines)):
      items = lines[i].split('\t')
      assert len(items) == 14
      coverage = items[3]
      perc1 = items[6]
      perc99 = items[-2]
      assert coverage.endswith('%')
      coverages.append(float(coverage[:-1]))
      perc1s.append(float(perc1))
      perc99s.append(float(perc99))
    coverage = sum(coverages)/len(coverages)
    perc1 = sum(perc1s)/len(perc1s)
    perc99 = sum(perc99s)/len(perc99s)
    print >> fp, '%s\t%.2f%%\t%.6f\t%.6f' % (
        feature, coverage, perc1, perc99)

