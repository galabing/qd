#!/usr/bin/python

import os

def run(cmd, dry_run=False):
  print 'running: %s' % cmd
  if dry_run:
    return
  assert os.system(cmd) == 0, 'command failed'

# [indicator, negate, [dimension ...]]
ITEMS = [
    # income
    ['REVENUE', False, ['ARQ', 'ART']],
    ['COR', False, ['ARQ', 'ART']],
    ['GP', False, ['ARQ', 'ART']],
    ['RND', False, ['ARQ', 'ART']],
    ['SGNA', False, ['ARQ', 'ART']],
    ['EBIT', False, ['ARQ', 'ART']],
    ['INTEXP', False, ['ARQ', 'ART']],
    ['EBT', False, ['ARQ', 'ART']],
    ['TAXEXP', False, ['ARQ', 'ART']],
    ['NETINC', False, ['ARQ', 'ART']],
    ['PREFDIVIS', False, ['ARQ', 'ART']],
    ['NETINCCMN', False, ['ARQ', 'ART']],
    ['NETINCDIS', False, ['ARQ', 'ART']],
    # cash flow
    ['NCFO', False, ['ARQ', 'ART']],
    ['DEPAMOR', False, ['ARQ', 'ART']],
    ['NCFI', False, ['ARQ', 'ART']],
    ['CAPEX', True, ['ARQ', 'ART']],  # negate
    ['NCFF', False, ['ARQ', 'ART']],
    ['NCFX', False, ['ARQ', 'ART']],
    ['NCF', False, ['ARQ', 'ART']],
    # balance
    ['ASSETS', False, ['ARQ']],
    ['ASSETSC', False, ['ARQ']],
    ['ASSETSNC', False, ['ARQ']],
    ['CASHNEQ', False, ['ARQ']],
    ['RECEIVABLES', False, ['ARQ']],
    ['INTANGIBLES', False, ['ARQ']],
    ['LIABILITIES', False, ['ARQ']],
    ['LIABILITIESC', False, ['ARQ']],
    ['LIABILITIESNC', False, ['ARQ']],
    ['DEBT', False, ['ARQ']],
    ['PAYABLES', False, ['ARQ']],
    ['EQUITY', False, ['ARQ']],
    ['ACCOCI', False, ['ARQ']],
    # metrics
    ['ASSETSAVG', False, ['ART']],
    ['EBITDA', False, ['ARQ', 'ART']],
    ['EQUITYAVG', False, ['ART']],
    ['EV', False, ['ND']],
    ['FCF', False, ['ARQ', 'ART']],
    ['MARKETCAP', False, ['ND']],
    ['TANGIBLES', False, ['ARQ']],
    ['WORKINGCAPITAL', False, ['ARQ']],
]
BIN_DIR = '/Users/lnyang/lab/qd/qd'
DATA_DIR = '/Users/lnyang/lab/qd/data'
DRY_RUN = False

count = 0
for indicator, negate, dimensions in ITEMS:
  for dimension in dimensions:
    negate_str = ''
    negate_flag = ''
    if negate:
      negate_str = '-'
      negate_flag = '--negate'
    feature_dir = '%s/features/log%s%s-%s' % (
        DATA_DIR, negate_str, indicator, dimension)
    if not os.path.isdir(feature_dir):
      os.mkdir(feature_dir)
    assert len(os.listdir(feature_dir)) == 0, 'non-empty dir: %s' % feature_dir
    cmd = ('%s/compute_log_feature.py '
           '--l1_dir=%s/sf1/l1 --ticker_file=%s/tickers --dimension=%s '
           '--header=%s %s --feature_dir=%s --info_file=%s/info' % (
           BIN_DIR, DATA_DIR, DATA_DIR, dimension, indicator, negate_flag,
           feature_dir, feature_dir))
    run(cmd, dry_run=DRY_RUN)
    count += 1
print 'finished %d commands' % count

