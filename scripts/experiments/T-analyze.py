#!/usr/bin/python

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

def writeKs(data, ks, output_file):
  with open(output_file, 'w') as fp:
    print >> fp, 'date\t%s' % ('\t'.join(['%d' % k for k in ks]))
    for date in sorted(data.keys()):
      items = [item[1] for item in data[date]]
      gains = []
      for k in ks:
        if k > 0:
          assert len(items) >= k
          p = 0
          q = k
        elif k == 0:
          p = 0
          q = len(items)
        else:
          assert len(items) >= -k
          p = len(items) + k
          q = len(items)
        gains.append(sum(items[p:q])/(q-p))
      print >> fp, '%s\t%s' % (date.replace('-', '/'),
                               '\t'.join(['%f' % g for g in gains]))

def writeBuckets(data, buckets, output_file):
  assert buckets > 0
  histogram = [0.0 for i in range(buckets)]
  for items in data.itervalues():
    gains = [item[1] for item in items]
    bucket_size = int(len(gains)/buckets)
    sizes = [bucket_size for i in range(buckets)]
    extra = len(gains) % buckets
    for i in range(buckets - extra, buckets):
      sizes[i] += 1
    assert sum(sizes) == len(gains)
    p = 0
    for i in range(buckets):
      size = sizes[i]
      histogram[i] += sum(gains[p:p+size]) / size
      p += size
  for i in range(buckets):
    histogram[i] /= len(data)
  with open(output_file, 'w') as fp:
    print >> fp, '%s\tavg' % ('\t'.join(['B%d' % (i+1) for i in range(buckets)]))
    print >> fp, '%s\t%f' % ('\t'.join(['%f' % h for h in histogram]), sum(histogram)/len(histogram))

input_dir = '/Users/lnyang/lab/qd/data/experiments/T/results'
output_dir = '%s/misc' % input_dir

versions = [60, 72, 84, 96, -1]
delays = [0]

ks = [3, 5, 10, 0, -10, -5, -3]
buckets = 10

for version in versions:
  for delay in delays:
    input_file = '%s/version_%d_delay_%d' % (input_dir, version, delay)
    data = readData(input_file)
    if ks is not None:
      writeKs(data, ks, '%s/topbot_%d_%d.tsv' % (output_dir, version, delay))
    if buckets is not None:
      writeBuckets(data, buckets, '%s/bkt%d_%d_%d.tsv' % (output_dir, buckets, version, delay))

