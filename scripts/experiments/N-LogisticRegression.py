#!/usr/bin/python

import exp_utils

trainer = '/Users/lnyang/lab/qd/qd/train_model.py'

base_dir = '/Users/lnyang/lab/qd/data/experiments/N'
train_dir = '%s/train' % base_dir
model_dir = '%s/models' % base_dir
validate_dir = '%s/validate' % base_dir

#percs = [0.4, 0.6, 0.8, 1.0]
#Cs = [0.1, 1.0, 10.0]

percs = [1.0]
Cs = [0.01, 0.03, 0.3, 3.0, 30.0, 100.0]

data_file = '%s/data' % train_dir
label_file = '%s/label' % train_dir

vdata_file = '%s/data' % validate_dir
vlabel_file = '%s/label' % validate_dir

info_file = '%s/LogisticRegression_info' % base_dir
info_fp = open(info_file, 'w')
print >> info_fp, '\t'.join(
    ['perc', 'C', 'train_precision', 'validate_precision', 'train_recall', 'validate_recall'])

for perc in percs:
  for C in Cs:
    # Train model.
    model_def = 'LogisticRegression(C=%f)' % C
    model_file = '%s/LogisticRegression-%f-%f' % (model_dir, perc, C)
    exp_utils.trainModel(trainer, data_file, label_file, model_def, perc,
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
        ['%f' % perc, '%f' % C, '%f' % train_precision,
         '%f' % validate_precision, '%f' % train_recall,
         '%f' % validate_recall])
    info_fp.flush()

info_fp.close()

