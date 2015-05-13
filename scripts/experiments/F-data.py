#!/usr/bin/python

import os

def run(cmd):
  print 'running command: %s' % cmd
  assert os.system(cmd) == 0

def collect(folder, min_date='0000-00-00', max_date='9999-99-99'):
  collector = '/Users/lnyang/lab/qd/qd/collect_reg_data.py'
  data_dir = '/Users/lnyang/lab/qd/data'
  exp_dir = '/Users/lnyang/lab/qd/data/experiments/F'
  folder_dir = '%s/%s' % (exp_dir, folder)

  ticker_file = '%s/tickers' % data_dir
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

collect('train', max_date='2010-12-31')
collect('validate', min_date='2012-01-01', max_date='2012-12-31')
collect('test', min_date='2014-01-01')

