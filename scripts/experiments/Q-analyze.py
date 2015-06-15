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
  total_histogram = [0.0 for i in range(buckets)]
  total_months = 0
  histograms = dict()  # year => histogram, months
  for date, items in data.iteritems():
    year, m = date.split('-')
    if year not in histograms:
      histograms[year] = [[0.0 for i in range(buckets)], 0]
    histograms[year][1] += 1
    histogram = histograms[year][0]

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
      gain = sum(gains[p:p+size]) / size
      histogram[i] += gain
      total_histogram[i] += gain
      p += size
    total_months += 1

  for histogram, months in histograms.itervalues():
    for i in range(buckets):
      histogram[i] /= months
  for i in range(buckets):
    total_histogram[i] /= total_months

  with open(output_file, 'w') as fp:
    print >> fp, 'year\t%s\tavg\tmonths' % ('\t'.join(['B%d' % (i+1) for i in range(buckets)]))
    for year in sorted(histograms.keys()):
      histogram, months = histograms[year]
      print >> fp, '%s\t%s\t%f\t%d' % (year, '\t'.join(['%f' % h for h in histogram]), sum(histogram)/len(histogram), months)
    print >> fp, 'all\t%s\t%f\t%d' % ('\t'.join(['%f' % h for h in total_histogram]), sum(total_histogram)/len(total_histogram), total_months)

input_dir = '/Users/lnyang/lab/qd/data/experiments/Q/results'
output_dir = '%s/misc' % input_dir

versions = [-1]
delays = [0]

ks = None  #[3, 5, 10, 30, 50, 100, 300, 500, 0, -500, -300, -100, -50, -30, -10, -5, -3]
buckets = 10

for version in versions:
  for delay in delays:
    input_file = '%s/version_%d_delay_%d' % (input_dir, version, delay)
    data = readData(input_file)
    if ks is not None:
      writeKs(data, ks, '%s/topbot_%d_%d.tsv' % (output_dir, version, delay))
    if buckets is not None:
      writeBuckets(data, buckets, '%s/bkt%d_%d_%d.tsv' % (output_dir, buckets, version, delay))

