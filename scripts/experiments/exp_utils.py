import numpy
import os
import pickle
import sys

def run(cmd):
  print 'running command: %s' % cmd
  sys.stdout.flush()
  assert os.system(cmd) == 0

def trainModel(trainer, data_file, label_file, model_def, perc, model_file):
  cmd = ('%s --data_file=%s --label_file=%s --model_def=\'%s\' --perc=%f '
         '--model_file=%s' % (trainer, data_file, label_file, model_def,
                              perc, model_file))
  run(cmd)

def computeError(model_file, data_file, label_file):
  print 'computing error for'
  print '  model: %s' % model_file
  print '  data: %s' % data_file
  print '  label: %s' % label_file
  with open(model_file, 'rb') as fp:
    model = pickle.load(fp)
  print 'model: %s' % model
  X = numpy.loadtxt(data_file)
  print 'X.shape: %s' % str(X.shape)
  y = numpy.loadtxt(label_file)
  print 'y.shape: %s' % str(y.shape)

  p = model.predict(X)
  m = X.shape[0]
  se = ((y - p) ** 2).sum()
  r2 = model.score(X, y)
  return m, se, r2

def getModels(model_dir):
  items = os.listdir(model_dir)
  models = []
  for item in items:
    alg, perc, alpha = item.split('-')
    if perc == '1.000000':
      models.append(item)
  return sorted(models)

def computeDetailedGainDistribution(
    model_file, data_file, label_file, meta_file, num_buckets):
  with open(model_file, 'rb') as fp:
    model = pickle.load(fp)
  print 'model: %s' % model

  X = numpy.loadtxt(data_file)
  print 'X.shape: %s' % str(X.shape)
  y = numpy.loadtxt(label_file)
  print 'y.shape: %s' % str(y.shape)

  p = model.predict(X)

  with open(meta_file, 'r') as fp:
    lines = fp.read().splitlines()
  assert len(lines) == y.shape[0]
  assert y.shape[0] == p.shape[0]

  meta_dict = dict()  # ym => [[predicted, gain] ...]
  for i in range(len(lines)):
    ticker, date, count = lines[i].split('\t')
    year, month, day = date.split('-')
    ym = '%s-%s' % (year, month)
    if ym not in meta_dict:
      meta_dict[ym] = [[p[i], y[i]]]
    else:
      meta_dict[ym].append([p[i], y[i]])
  print 'aggregating %d dates from %s to %s' % (
      len(meta_dict), min(meta_dict.keys()), max(meta_dict.keys()))

  distrs = dict()
  for ym, items in meta_dict.iteritems():
    distr = [0.0 for i in range(num_buckets)]
    items = sorted(items, key=lambda item: item[0], reverse=True)
    bucket_size = len(items) / num_buckets
    print '%s: %d tickers, %d per bucket' % (
        ym, len(items), bucket_size)
    for i in range(num_buckets):
      start = bucket_size * i
      end = start + bucket_size
      if i == num_buckets - 1:
        end = len(items)
      gains = [items[j][1] for j in range(start, end)]
      distr[i] = sum(gains) / len(gains)
    distrs[ym] = distr
  return distrs

def computeGainDistribution(
    model_file, data_file, label_file, meta_file, num_buckets):
  distrs = computeDetailedGainDistribution(
      model_file, data_file, label_file, meta_file, num_buckets)
  distr = [0.0 for i in range(num_buckets)]
  for row in distrs.itervalues():
    for i in range(num_buckets):
      distr[i] += row[i]
  for i in range(num_buckets):
    distr[i] /= len(distrs)
  return distr

