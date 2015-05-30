#!/usr/bin/python

import exp_utils

trainer = '/Users/lnyang/lab/qd/qd/train_model2.py'

base_dir = '/Users/lnyang/lab/qd/data/experiments/Q'
all_dir = '%s/all' % base_dir
model_dir = '%s/models' % base_dir

n_estimators = 100
max_depth = 2

# earliest date is 2004-01 => earliest yyyymm is 200412 predicting 200512
# latest is 2014-05 => latest yyyymm is 201305 predicting 201405
# try 12, 24, 36, 48, inf (-1); for earlier years data may not be available
first_ym = '200412'
last_ym = '201305'
months = [12, 24, 36, 48, -1]

n_estimators_list = [100, 1000]
max_depth_list = [1, 2, 3, 4]

data_file = '%s/data' % all_dir
label_file = '%s/label' % all_dir
meta_file = '%s/meta' % all_dir

info_file = '%s/RandomForestClassifier_info' % base_dir
info_fp = open(info_file, 'w')
print >> info_fp, '\t'.join(
    ['n_estimators', 'max_depth', 'yyyymm', 'months', 'train_precision', 'train_recall'])

yyyymms = []
yyyymm = first_ym
while yyyymm <= last_ym:
  yyyymms.append(yyyymm)
  y = int(yyyymm[:4])
  m = int(yyyymm[4:])
  if m < 12:
    m += 1
  else:
    m = 1
    y += 1
  yyyymm = '%04d%02d' % (y, m)
print 'yyyymms: %s' % yyyymms
print 'months: %s' % months

TMP_DATA_FILE = '/tmp/qd_tmp_data'
TMP_LABEL_FILE = '/tmp/qd_tmp_label'

for yyyymm in yyyymms:
  for month in months:
    # Train model.
    model_def = 'RandomForestClassifier(n_estimators=%d, max_depth=%d)' % (n_estimators, max_depth)
    model_file = '%s/RandomForestClassifier-%d-%d-%s-%d' % (model_dir, n_estimators, max_depth, yyyymm, month)
    exp_utils.trainModel2(trainer, data_file, label_file, meta_file, yyyymm, month, model_def, 1.0, model_file)

    # Compute training error.
    train_tp, train_tn, train_fp, train_fn = exp_utils.computeClsError(
        model_file, TMP_DATA_FILE, TMP_LABEL_FILE)
    train_precision = float(train_tp) / (train_tp + train_fp)
    train_recall = float(train_tp) / (train_tp + train_fn)

    print >> info_fp, '\t'.join(
        ['%d' % n_estimators, '%d' % max_depth, '%s' % yyyymm, '%d' % month, 
         '%f' % train_precision, '%f' % train_recall])
    info_fp.flush()

info_fp.close()

