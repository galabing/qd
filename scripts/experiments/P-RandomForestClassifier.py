#!/usr/bin/python

import exp_utils

trainer = '/Users/lnyang/lab/qd/qd/train_model.py'

base_dir = '/Users/lnyang/lab/qd/data/experiments/P'
train_dir = '%s/train' % base_dir
model_dir = '%s/models' % base_dir
validate_dir = '%s/validate' % base_dir

n_estimators_list = [100, 1000]
max_depth_list = [1, 2, 3, 4]

data_file = '%s/data' % train_dir
label_file = '%s/label' % train_dir

vdata_file = '%s/data' % validate_dir
vlabel_file = '%s/label' % validate_dir

info_file = '%s/RandomForestClassifier_info' % base_dir
info_fp = open(info_file, 'w')
print >> info_fp, '\t'.join(
    ['n_estimators', 'max_depth', 'train_precision', 'validate_precision', 'train_recall', 'validate_recall'])

for n_estimators in n_estimators_list:
  for max_depth in max_depth_list:
    # Train model.
    model_def = 'RandomForestClassifier(n_estimators=%d, max_depth=%d)' % (n_estimators, max_depth)
    model_file = '%s/RandomForestClassifier-%d-%d' % (model_dir, n_estimators, max_depth)
    exp_utils.trainModel(trainer, data_file, label_file, model_def, 1.0,
                         model_file)

    # Compute training error.
    train_tp, train_tn, train_fp, train_fn = exp_utils.computeClsError(
        model_file, data_file, label_file)
    train_precision = float(train_tp) / (train_tp + train_fp)
    train_recall = float(train_tp) / (train_tp + train_fn)

    # Compute validation error.
    validate_tp, validate_tn, validate_fp, validate_fn = exp_utils.computeClsError(
        model_file, vdata_file, vlabel_file)
    validate_precision = float(validate_tp) / (validate_tp + validate_fp)
    validate_recall = float(validate_tp) / (validate_tp + validate_fn)

    print >> info_fp, '\t'.join(
        ['%d' % n_estimators, '%d' % max_depth, '%f' % train_precision,
         '%f' % validate_precision, '%f' % train_recall,
         '%f' % validate_recall])
    info_fp.flush()

info_fp.close()

