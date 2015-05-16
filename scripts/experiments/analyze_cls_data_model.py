#!/usr/bin/python

import numpy
import pickle

def inspectData(data_dir):
  data = numpy.loadtxt('%s/data' % data_dir)
  label = numpy.loadtxt('%s/label' % data_dir)
  npos = sum(label)
  perc = float(npos) * 100 / len(label)
  print '  %d data points' % len(label)
  print '  %d positive (%.2f%%)' % (npos, perc)
  with open('%s/meta' % data_dir, 'r') as fp:
    lines = fp.read().splitlines()
  meta = []
  gains = []
  for line in lines:
    ticker, date, count, gain = line.split('\t')
    gain = float(gain)
    meta.append([ticker, date, gain])
    gains.append(gain * 100)
  gains = sorted(gains, reverse=True)
  print '  1%% (maybe excess) gain: %.2f%%, 99%%: %.2f%%; avg: %.2f%%' % (
      gains[int(len(gains)*0.01)], gains[int(len(gains)*0.99)],
      sum(gains)/len(gains))
  return data, label, meta

def inspectModel(model_file, fl_file):
  with open(model_file, 'rb') as fp:
    model = pickle.load(fp)
  print '  %s' % str(model)
  with open(fl_file, 'r') as fp:
    features = [line for line in fp.read().splitlines()
                if not line.startswith('#')]
  coef = model.coef_[0]
  assert len(features) == len(coef)
  feature_coef = [[features[i], coef[i]] for i in range(len(features))]
  feature_coef.sort(key=lambda item: abs(item[1]), reverse=True)
  print '%d feature coeffs:' % len(feature_coef)
  if len(feature_coef) <= 200:
    for feature, coef in feature_coef:
      print '  %s: %f' % (feature, coef)
  else:
    for i in range(10):
      print '  %s: %f' % (feature_coef[i][0], feature_coef[i][1])
    print ' ...'
    for i in range(-10, 0):
      print '  %s: %f' % (feature_coef[i][0], feature_coef[i][1])
  print 'intercept: %f' % model.intercept_
  return model

def analyze(model, data, label, meta, per_month, percs):
  prob = model.predict_proba(data)
  prob = [item[1] for item in prob]

  observed = sum(label)
  expected = sum(prob)
  print '  observed = %f, expected = %f, ratio = %f' % (
      observed, expected, observed/expected)

  items_dict = dict()  # ym => [[prob, label, gain, ticker, date] ...]
  for i in range(len(prob)):
    if per_month:
      y, m, d = meta[i][1].split('-')
      ym = '%s-%s' % (y, m)
    else:
      ym = 'all'
    if ym not in items_dict:
      items_dict[ym] = []
    items_dict[ym].append(
        [prob[i], label[i], meta[i][2], meta[i][0], meta[i][1]])

  for ym in sorted(items_dict.keys()):
    print
    print ' == date: %s ==' % ym
    items = sorted(items_dict[ym], key=lambda item: item[0], reverse=True)
    print '  %d items, high score = %f, low score = %f' % (
        len(items), items[0][0], items[-1][0])
    tp, tn, fp, fn = 0.0, 0.0, 0.0, 0.0
    for item in items:
      if item[0] > 0.5:
        if item[1] > 0.5:
          tp += 1
        else:
          fp += 1
      else:
        if item[1] > 0.5:
          fn += 1
        else:
          tn += 1
    print '  with threshold = 0.5:'
    print '    precision = %.2f%%' % (tp*100/(tp+fp))
    print '    recall = %.2f%%' % (tp*100/(tp+fn))
    print '    accuracy = %.2f%%' % ((tp+tn)*100/(tp+tn+fp+fn))
    gains = [item[2] for item in items]
    print '  groundtruth: %.2f%% positives, %.2f%% mean gain' % (
        (tp+fn)*100/(tp+tn+fp+fn), sum(gains)*100/len(gains))
    for perc in percs:
      index = int(len(items) * perc)
      tickers = set()
      for item in items[:index+1]:
        tickers.add(item[3])
      print '  top %.2f%%:' % (perc*100)
      print '    score = %f' % items[index][0]
      print '    count = %d (%d unique tickers)' % (index + 1, len(tickers))
      positives = sum([item[1] for item in items[:index+1]])
      precision = float(positives)/(index+1)
      print '    positives = %d (precision = %.2f%%)' % (
          positives, precision*100)
      gains = [item[2] for item in items[:index+1]]
      gain = sum(gains)/len(gains)
      print '    mean gain = %.2f%%' % (gain*100)
      #if index < 40:
      #  print '    sample transactions:'
      #  for item in items[:index+1]:
      #    print '      %s %s: %.2f%%' % (
      #        item[3], item[4], item[2]*100)

exp_dir = '/Users/lnyang/lab/qd/data/experiments/N'

model_dir = '%s/models' % exp_dir
model = 'LogisticRegression-1.000000-1.000000'

fl_file = '%s/feature_list' % exp_dir
train_dir = '%s/train' % exp_dir
validate_dir = '%s/validate' % exp_dir
test_dir = '%s/test' % exp_dir

percs = [0.001, 0.01, 0.1, 0.5]
per_month = True

print 'inspecting training data...'
data, label, meta = inspectData(train_dir)

print 'inspecting validation data...'
vdata, vlabel, vmeta = inspectData(validate_dir)

print 'inspecting testing data...'
tdata, tlabel, tmeta = inspectData(test_dir)

print 'inspecting model...'
model = inspectModel('%s/%s' % (model_dir, model), fl_file)

print 'training results...'
analyze(model, data, label, meta, False, percs)

print 'validation results...'
analyze(model, vdata, vlabel, vmeta, per_month, percs)

print 'testing results...'
analyze(model, tdata, tlabel, tmeta, per_month, percs)

