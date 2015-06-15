#!/usr/bin/python

""" Merges volatility data from all tickers and produce a map:
    (ticker, ym) => (volatility, rank) where
    rank = 0-based-position / total_tickers_on_ym
    Lower rank corresponds to higher volatility.
"""

import os
import pickle

base_dir = '/Users/lnyang/lab/qd/data/fvolatilities'
k = 12
input_dir = '%s/%d' % (base_dir, k)
output_file = '%s/map%d.pkl' % (base_dir, k)

tickers = sorted(os.listdir(input_dir))
print 'processing %d tickers' % len(tickers)

data1 = dict()  # ym => [[ticker, volatility] ...]
for ticker in tickers:
  print ticker
  with open('%s/%s' % (input_dir, ticker), 'r') as fp:
    lines = fp.read().splitlines()
  for line in lines:
    ymd, volatility = line.split('\t')
    y, m, d = ymd.split('-')
    ym = '%s-%s' % (y, m)
    value = [ticker, float(volatility)]
    if ym not in data1:
      data1[ym] = [value]
    else:
      data1[ym].append(value)

data2 = dict()  # (ticker, ym) => (volatility, rank)
for ym in sorted(data1.keys()):
  print ym
  items = data1[ym]
  items.sort(key=lambda item: item[1], reverse=True)
  denom = float(len(items))
  for i in range(len(items)):
    key = (items[i][0], ym)
    value = (items[i][1], i/denom)
    assert key not in data2
    data2[key] = value

print '%d entries in map' % (len(data2))
with open(output_file, 'wb') as fp:
  pickle.dump(data2, fp)

