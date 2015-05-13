#!/usr/bin/python

import exp_utils

trainer = '/Users/lnyang/lab/qd/qd/train_model.py'
exp_dir = '/Users/lnyang/lab/qd/data/experiments/H'

percs = [0.2, 0.4, 0.6, 0.8, 1.0]
alphas = [0.01, 0.1, 1.0, 10.0, 100.0]

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
  base_dir = '%s/%s' % (exp_dir, sector)

  train_dir = '%s/train' % base_dir
  model_dir = '%s/models' % base_dir
  validate_dir = '%s/validate' % base_dir

  data_file = '%s/data' % train_dir
  label_file = '%s/label' % train_dir

  vdata_file = '%s/data' % validate_dir
  vlabel_file = '%s/label' % validate_dir

  info_file = '%s/Ridge_info' % base_dir
  info_fp = open(info_file, 'w')
  print >> info_fp, '\t'.join(
      ['perc', 'alpha', 'train_mse', 'validate_mse', 'train_r2', 'validate_r2'])

  for perc in percs:
    for alpha in alphas:
      # Train model.
      model_def = ('Ridge(alpha=%f, fit_intercept=True, normalize=False,'
                   ' copy_X=False, solver="cholesky")' % alpha)
      model_file = '%s/Ridge-%f-%f' % (model_dir, perc, alpha)
      exp_utils.trainModel(trainer, data_file, label_file, model_def, perc,
                           model_file)

      # Compute training error.
      train_m, train_se, train_r2 = exp_utils.computeError(
          model_file, data_file, label_file)

      # Compute validation error.
      validate_m, validate_se, validate_r2 = exp_utils.computeError(
          model_file, vdata_file, vlabel_file)

      print >> info_fp, '\t'.join(
          ['%f' % perc, '%f' % alpha, '%f' % (train_se/train_m),
           '%f' % (validate_se/validate_m), '%f' % train_r2,
           '%f' % validate_r2])
      info_fp.flush()

  info_fp.close()

