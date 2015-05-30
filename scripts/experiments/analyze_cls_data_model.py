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

  if hasattr(model, 'coef_'):
    scores = model.coef_[0]
  elif hasattr(model, 'feature_importances_'):
    scores = model.feature_importances_
  else:
    return model

  with open(fl_file, 'r') as fp:
    features = [line for line in fp.read().splitlines()
                if not line.startswith('#')]
  assert len(features) == len(scores)
  feature_scores = [[features[i], scores[i]] for i in range(len(features))]
  feature_scores.sort(key=lambda item: abs(item[1]), reverse=True)
  print '%d feature scores:' % len(feature_scores)
  if len(feature_scores) <= 200:
    for feature, score in feature_scores:
      print '  %s: %f' % (feature, score)
  else:
    for i in range(10):
      print '  %s: %f' % (feature_scores[i][0], feature_scores[i][1])
    print ' ...'
    for i in range(-10, 0):
      print '  %s: %f' % (feature_scores[i][0], feature_scores[i][1])
  if hasattr(model, 'intercept_'):
    print 'intercept: %f' % model.intercept_
  return model

def analyze(model, data, label, meta, per_month, percs, num_buckets):
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
      if len(tickers) <= 5:
        ticker_str = ', '.join(sorted(tickers))
      else:
        stickers = sorted(tickers)
        ticker_str = '%s, %s, ..., %s, %s' % (stickers[0], stickers[1],
                                              stickers[-2], stickers[-1])
      print '    count = %d (%d unique tickers): %s' % (
          index + 1, len(tickers), ticker_str)
      positives = sum([item[1] for item in items[:index+1]])
      precision = float(positives)/(index+1)
      print '    positives = %d (precision = %.2f%%)' % (
          positives, precision*100)
      perc_gains = gains[:index+1]
      gain = sum(perc_gains)/len(perc_gains)
      print '    mean gain = %.2f%%' % (gain*100)
    if num_buckets > 0:
      bucket_size = int(len(items) / num_buckets)
      assert bucket_size > 0
      bucket_gains = []
      for i in range(num_buckets):
        start_index = bucket_size * i
        if i == num_buckets - 1:
          end_index = len(items)
        else:
          end_index = start_index + bucket_size
        gain = sum(gains[start_index:end_index]) / (end_index - start_index)
        bucket_gains.append(gain)
      print '  %d buckets' % num_buckets
      print ' '.join(['%.2f%%' % (gain*100) for gain in bucket_gains])
      if bucket_size <= 30:  # print the first bucket
        print '  top bucket:'
        for i in range(bucket_size):
          print items[i]
        print '  bottom bucket:'
        for i in range(len(items)-bucket_size, len(items)):
          print items[i]

exp_dir = '/Users/lnyang/lab/qd/data/experiments/P'

model_dir = '%s/models' % exp_dir
model = 'RandomForestClassifier-100-2'

fl_file = '%s/feature_list' % exp_dir
train_dir = '%s/train' % exp_dir
validate_dir = '%s/validate' % exp_dir
test_dir = '%s/test' % exp_dir

percs = [0.001, 0.01, 0.1, 0.5]
num_buckets = 10
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
analyze(model, data, label, meta, False, percs, num_buckets)

print 'validation results...'
analyze(model, vdata, vlabel, vmeta, per_month, percs, num_buckets)

print 'testing results...'
analyze(model, tdata, tlabel, tmeta, per_month, percs, num_buckets)

