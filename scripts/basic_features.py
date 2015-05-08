#!/usr/bin/python

import os

def run(cmd, dry_run=False):
  print 'running: %s' % cmd
  if dry_run:
    return
  assert os.system(cmd) == 0, 'command failed'

# [indicator, [dimension ...]]
ITEMS = [
    ['ASSETTURNOVER', ['ART']],
    ['CURRENTRATIO', ['ARQ']],
    ['DE', ['ARQ']],
    ['DILUTIONRATIO', ['ARQ', 'ART']],
    ['DIVYIELD', ['ND']],
    ['EBITDAMARGIN', ['ART']],
    ['EPSDILGROWTH1YR', ['ART']],
    ['EPSGROWTH1YR', ['ART']],
    ['EVEBIT', ['ART']],
    ['EVEBITDA', ['ART']],
    ['GROSSMARGIN', ['ART']],
    ['INTERESTBURDEN', ['ART']],
    ['LEVERAGERATIO', ['ART']],
    ['NCFOGROWTH1YR', ['ART']],
    ['NETINCGROWTH1YR', ['ART']],
    ['NETMARGIN', ['ART']],
    ['PE', ['ART']],
    ['PE1', ['ART']],
    ['PS1', ['ART']],
    ['PS', ['ART']],
    ['PB', ['ARQ']],
    ['REVENUEGROWTH1YR', ['ART']],
    ['SHARESWAGROWTH1YR', ['ART']],
    ['PAYOUTRATIO', ['ART']],
    ['ROA', ['ART']],
    ['ROE', ['ART']],
    ['ROS', ['ART']],
    ['TAXEFFICIENCY', ['ART']],
]
BIN_DIR = '/Users/lnyang/lab/qd/qd'
DATA_DIR = '/Users/lnyang/lab/qd/data'
DRY_RUN = False

count = 0
for indicator, dimensions in ITEMS:
  for dimension in dimensions:
    feature_dir = '%s/features/%s-%s' % (DATA_DIR, indicator, dimension)
    if not os.path.isdir(feature_dir):
      os.mkdir(feature_dir)
    assert len(os.listdir(feature_dir)) == 0, 'non-empty dir: %s' % feature_dir
    cmd = ('%s/compute_basic_feature.py '
           '--l1_dir=%s/sf1/l1 --ticker_file=%s/tickers --dimension=%s '
           '--header=%s --feature_dir=%s --info_file=%s/info' % (
           BIN_DIR, DATA_DIR, DATA_DIR, dimension, indicator, feature_dir,
           feature_dir))
    run(cmd, dry_run=DRY_RUN)
    count += 1
print 'finished %d commands' % count

