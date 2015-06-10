#!/usr/bin/python

""" Simulates training/prediction over time.

    For each version of the model (version being training period in months),
    stocks from each yyyymm will be grouped for prediction, and the model
    with right version, date (prediction date - prediction window - delay)
    will be used.  All stocks on that date will be scored and output will
    be written in the form of:
      date: yyyymm
      \tABC\tgain\tscore
      ...
      \tXYZ\tgain\tscore
    which can be used to simulate trading.
"""

import numpy
import os
import pickle
import sys
sys.path.append('/Users/lnyang/lab/qd/qd')
import utils

def getModelName(ym, version):
  y, m = ym.split('-')
  yyyymm = '%s%s' % (y, m)
  return 'RandomForestClassifier-100-2-%s-%d' % (yyyymm, version)

def prepareData(ym, data_file, label_file, meta_file, tmp_data_file):
  data_ifp = open(data_file, 'r')
  label_ifp = open(label_file, 'r')
  meta_ifp = open(meta_file, 'r')
  data_ofp = open(tmp_data_file, 'w')

  meta = []
  while True:
    line = meta_ifp.readline()
    if line == '':
      assert data_ifp.readline() == ''
      assert label_ifp.readline() == ''
      break
    assert line[-1] == '\n'
    data_line = data_ifp.readline()
    label_line = label_ifp.readline()
    assert data_line != ''
    assert label_line != ''
    ticker, date, tmp, gain = line[:-1].split('\t')
    if utils.getYm(date) != ym:
      continue
    assert data_line[-1] == '\n'
    assert label_line[-1] == '\n'
    label = float(label_line[:-1])
    gain = float(gain)
    if label > 0.5: assert gain >= 0
    if label < 0.5: assert gain <= 0
    print >> data_ofp, data_line[:-1]
    meta.append([ticker, gain])

  data_ifp.close()
  label_ifp.close()
  meta_ifp.close()
  data_ofp.close()
  return meta

exp_dir = '/Users/lnyang/lab/qd/data/experiments/U'
data_dir = '%s/all' % exp_dir
model_dir = '%s/models' % exp_dir
result_dir = '%s/results' % exp_dir

tmp_data_file = '/tmp/results_tmp_data'

versions = [-1]  # model versions (training period in months)
window = 12  # window of prediction in months

delay = 0  # delay in months
# eg, in predicting for 201406 with window=12 and delay=1,
# model from 201305 will be used (201406 - 12m - 1m).

data_file = '%s/data' % data_dir
label_file = '%s/label' % data_dir
meta_file = '%s/meta' % data_dir

# get dates for prediction
with open(meta_file, 'r') as fp:
  lines = fp.read().splitlines()
dates = set()
for line in lines:
  tmp1, date, tmp2, tmp3 = line.split('\t')
  dates.add(utils.getYm(date))
dates = sorted(dates)
print 'processing %d dates: %s' % (len(dates), dates)

fps = {version: open('%s/version_%d_delay_%d' % (result_dir, version, delay), 'w')
       for version in versions}

started = False  # check no 'hole' in simulation period
delta = window + delay
for date in dates:
  print 'processing %s' % date
  ym = utils.getPreviousYm(date, delta)
  print '  model from %s' % ym

  first = True  # data is lazily collected for the first model
  for version in versions:
    model_name = getModelName(ym, version)
    model_file = '%s/%s' % (model_dir, model_name)
    if not os.path.isfile(model_file):
      assert not started
      continue
    started = True

    if first:
      meta = prepareData(date, data_file, label_file, meta_file, tmp_data_file)
      print '  prepared %d data points' % len(meta)
    first = False

    data = numpy.loadtxt(tmp_data_file)
    assert data.shape[0] == len(meta)

    with open(model_file, 'rb') as fp:
      model = pickle.load(fp)
    print '  using model %s' % model_file
    prob = model.predict_proba(data)
    prob = [item[1] for item in prob]

    assert len(prob) == len(meta)
    items = [[meta[i][0], meta[i][1], prob[i]]
             for i in range(len(prob))]
    items.sort(key=lambda item: item[2], reverse=True)
    print >> fps[version], 'date: %s' % date
    for item in items:
      ticker, gain, score = item
      print >> fps[version], '\t%s\t%f\t%f' % (ticker, gain, score)

for fp in fps.itervalues():
  fp.close()

