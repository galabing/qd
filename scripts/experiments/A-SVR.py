#!/usr/bin/python

import exp_utils

trainer = '/Users/lnyang/lab/qd/qd/train_model.py'

base_dir = '/Users/lnyang/lab/qd/data/experiments/A'
train_dir = '%s/train' % base_dir
model_dir = '%s/models' % base_dir
validate_dir = '%s/validate' % base_dir

Cs = [0.1, 1.0, 10.0]
epsilons = [0.001, 0.01, 0.1]

data_file = '%s/data' % train_dir
label_file = '%s/label' % train_dir

vdata_file = '%s/data' % validate_dir
vlabel_file = '%s/label' % validate_dir

info_file = '%s/SVR_info' % base_dir
info_fp = open(info_file, 'w')
print >> info_fp, '\t'.join(
    ['perc', 'alpha', 'train_mse', 'validate_mse', 'train_r2', 'validate_r2'])

for C in Cs:
  for epsilon in epsilons:
    # Train model.
    model_def = ('SVR(C=%f, epsilon=%f, cache_size=1000)' % (C, epsilon))
    model_file = '%s/SVR-%f-%f' % (model_dir, C, epsilon)
    exp_utils.trainModel(trainer, data_file, label_file, model_def, 1.0,
                         model_file)

    # Compute training error.
    train_m, train_se, train_r2 = exp_utils.computeError(
        model_file, data_file, label_file)

    # Compute validation error.
    validate_m, validate_se, validate_r2 = exp_utils.computeError(
        model_file, vdata_file, vlabel_file)

    print >> info_fp, '\t'.join(
        ['%f' % C, '%f' % epsilon, '%f' % (train_se/train_m),
         '%f' % (validate_se/validate_m), '%f' % train_r2,
         '%f' % validate_r2])
    info_fp.flush()

info_fp.close()

