#!/usr/bin/python

ticker_file = '/Users/lnyang/lab/qd/data/tickers'
gain_dir = '/Users/lnyang/lab/qd/data/tmp/gains10/12'

min_date = '2004-01-01'
max_date = '9999-99-99'

with open(ticker_file, 'r') as fp:
  tickers = sorted(fp.read().splitlines())
print 'processing %d tickers' % len(tickers)

stats = dict()  # y => [gain ...]
for ticker in tickers:
  gain_file = '%s/%s' % (gain_dir, ticker)
  with open(gain_file, 'r') as fp:
    lines = fp.read().splitlines()
  for line in lines:
    date, gain = line.split('\t')
    if date < min_date or date > max_date:
      continue
    y, m, d = date.split('-')
    gain = float(gain)
    if gain > 100:
      print '!! %s %s: gain = %f' % (ticker, date, gain)
    if y not in stats: stats[y] = []
    stats[y].append(gain)

for y in sorted(stats.keys()):
  gains = sorted(stats[y])
  print '%s: %d data points, min/max/avg gain: %f / %f / %f' % (
      y, len(gains), min(gains), max(gains), sum(gains)/len(gains))
  print '  1%%: %f, 10%%: %f, 25%%: %f, 50%%: %f, 75%%: %f, 90%%: %f, 99%%: %f' % (
      gains[int(len(gains)*0.01)],
      gains[int(len(gains)*0.1)],
      gains[int(len(gains)*0.25)],
      gains[int(len(gains)*0.5)],
      gains[int(len(gains)*0.75)],
      gains[int(len(gains)*0.9)],
      gains[int(len(gains)*0.99)])

