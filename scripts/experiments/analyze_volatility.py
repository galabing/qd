#!/usr/bin/python

import pickle

def readData(input_file):
  # date => [[ticker, gain, score] ...]
  with open(input_file, 'r') as fp:
    lines = fp.read().splitlines()
  data = dict()
  for line in lines:
    if line.startswith('date:'):
      tmp, date = line.split(' ')
      assert date not in data
      data[date] = []
      continue
    empty, ticker, gain, score = line.split('\t')
    assert empty == ''
    gain = float(gain)
    score = float(score)
    if len(data[date]) > 0:
      assert score <= data[date][-1][2]
    data[date].append([ticker, gain, score])
  return data

vmap_file = '/Users/lnyang/lab/qd/data/fvolatilities/map12.pkl'
input_dir = '/Users/lnyang/lab/qd/data/experiments/Q/results'
output_dir = '%s/misc' % input_dir
versions = [-1]
delays = [0]
num_buckets = 10
k = 10  # calculate mean volatility rank for top and bottom k

with open(vmap_file, 'rb') as fp:
  vmap = pickle.load(fp)

for version in versions:
  for delay in delays:
    input_file = '%s/version_%d_delay_%d' % (input_dir, version, delay)
    data = readData(input_file)

    bkt_data = dict()  # year => histogram, months
    topbot_data = dict()  # year => histogram, months
    for date, items in data.iteritems():
      year, _ = date.split('-')
      if year not in bkt_data:
        bkt_data[year] = [[0.0 for i in range(num_buckets)], 0]
        assert year not in topbot_data
        topbot_data[year] = [[0.0, 0.0], 0]
      assert year in topbot_data
      bkt_histogram = bkt_data[year][0]
      topbot_histogram = topbot_data[year][0]
      bkt_data[year][1] += 1
      topbot_data[year][1] += 1

      bucket_size = int(len(items) / num_buckets)
      extra = len(items) % num_buckets
      bucket_sizes = []
      for i in range(num_buckets - extra):
        bucket_sizes.append(bucket_size)
      for i in range(num_buckets - extra, num_buckets):
        bucket_sizes.append(bucket_size + 1)
      assert sum(bucket_sizes) == len(items)

      volatilities = []
      ranks = []
      for ticker, _, _ in items:
        volatility, rank = vmap[(ticker, date)]
        volatilities.append(volatility)
        ranks.append(rank)

      p = 0
      for i in range(num_buckets):
        q = p + bucket_sizes[i]
        bkt_histogram[i] = sum(volatilities[p:q])/bucket_sizes[i]
        p = q
      topbot_histogram[0] += sum(ranks[:k])/k
      topbot_histogram[1] += sum(ranks[-k:])/k

    for histogram, months in bkt_data.itervalues():
      for i in range(num_buckets):
        histogram[i] /= months
    for histogram, months in topbot_data.itervalues():
      histogram[0] /= months
      histogram[1] /= months

    bkt_file = '%s/vbkt%d_%d_%d.tsv' % (output_dir, num_buckets, version, delay)
    topbot_file = '%s/vtopbot%d_%d_%d.tsv' % (output_dir, k, version, delay)
    bkt_fp = open(bkt_file, 'w')
    topbot_fp = open(topbot_file, 'w')

    print >> bkt_fp, 'year\t%s\tavg\tmonths' % ('\t'.join(['B%d' % (i+1) for i in range(num_buckets)]))
    print >> topbot_fp, 'year\ttop%d\tbot%d\tmonths' % (k, k)

    for year in sorted(bkt_data.keys()):
      histogram, months = bkt_data[year]
      print >> bkt_fp, '%s\t%s\t%.4f\t%d' % (
          year, '\t'.join(['%.4f' % h for h in histogram]), sum(histogram)/len(histogram), months)
    for year in sorted(topbot_data.keys()):
      histogram, months = topbot_data[year]
      top, bot = histogram
      print >> topbot_fp, '%s\t%.4f\t%.4f\t%d' % (year, top, bot, months)

    bkt_fp.close()
    topbot_fp.close()

