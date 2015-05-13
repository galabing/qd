#!/usr/bin/python

import os

def run(cmd):
  print 'running command: %s' % cmd
  assert os.system(cmd) == 0

def collect(sector, folder, min_date='0000-00-00', max_date='9999-99-99'):
  collector = '/Users/lnyang/lab/qd/qd/collect_reg_data.py'
  data_dir = '/Users/lnyang/lab/qd/data'
  exp_dir = '/Users/lnyang/lab/qd/data/experiments/H'
  folder_dir = '%s/%s/%s' % (exp_dir, sector, folder)
  if not os.path.isdir(folder_dir):
    os.makedirs(folder_dir)

  ticker_file = '%s/ticker_groups/sectors/sector_%s' % (data_dir, sector)
  gain_dir = '%s/egains10R3000/12' % data_dir
  feature_base_dir = '%s/features' % data_dir
  feature_list = '%s/feature_list' % exp_dir
  feature_stats = '%s/misc/stats.tsv' % feature_base_dir

  data_file = '%s/data' % folder_dir
  label_file = '%s/label' % folder_dir
  meta_file = '%s/meta' % folder_dir

  cmd = ('%s --ticker_file=%s --gain_dir=%s --feature_base_dir=%s '
         '--feature_list=%s --feature_stats=%s --min_date=%s '
         '--max_date=%s --data_file=%s --label_file=%s --meta_file=%s' % (
             collector, ticker_file, gain_dir, feature_base_dir,
             feature_list, feature_stats, min_date, max_date,
             data_file, label_file, meta_file))
  run(cmd)

sectors = [
    'Basic-Materials',
    'Consumer-Goods',
    'Financial',
    'Healthcare',
    'Industrial-Goods',
    'Services',
    'Technology',
    'Utilities',
]

for sector in sectors:
  collect(sector, 'train', max_date='2010-12-31')
  collect(sector, 'validate', min_date='2011-02-01', max_date='2012-12-31')
  collect(sector, 'test', min_date='2013-02-01')

