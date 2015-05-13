#!/usr/bin/python

import exp_utils

base_dir = '/Users/lnyang/lab/qd/data/experiments/H'
folder = 'test'
model = 'Ridge-1.000000-1.000000'
num_buckets = 10

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
  exp_dir = '%s/%s' % (base_dir, sector)
  model_dir = '%s/models' % exp_dir
  folder_dir = '%s/%s' % (exp_dir, folder)
  data_file = '%s/data' % folder_dir
  label_file = '%s/label' % folder_dir
  meta_file = '%s/meta' % folder_dir
  plot_file = '%s/plot.png' % folder_dir

  distr_file = '%s/distr-%d.tsv' % (folder_dir, num_buckets)

  print 'testing %s with %d buckets' % (model, num_buckets)

  distr_fp = open(distr_file, 'w')
  print >> distr_fp, 'date\t%s\tavg' % ('\t'.join([
      str(i) for i in range(1, num_buckets+1)]))

  model_file = '%s/%s' % (model_dir, model)
  distrs = exp_utils.computeDetailedGainDistribution(
      model_file, data_file, label_file, meta_file, num_buckets, plot_file)
  for ym in sorted(distrs.keys()):
    distr = distrs[ym]
    avg = sum(distr)/len(distr)
    print >> distr_fp, '%s\t%s\t%f' % (
        ym, '\t'.join(['%f' % d for d in distr]), avg)
  distr_fp.close()

