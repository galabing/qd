#!/usr/bin/python

""" Calculates data distribution histogram date => #tickers with data.
"""

import os

def updateDistr(distr, date):
  if date not in distr:
    distr[date] = 1
  else:
    distr[date] += 1

def getNextDate(date):
  y, m = date.split('-')
  y = int(y)
  m = int(m)
  if m < 12:
    m += 1
  else:
    y += 1
    m = 1
  return '%04d-%02d' % (y, m)

raw_dir = '/Users/lnyang/lab/qd/data/eod/raw'
distr_file = '/Users/lnyang/lab/qd/data/eod/misc/distr.tsv'

tickers = sorted(os.listdir(raw_dir))
print 'processing %d tickers' % len(tickers)

distr = dict()
for ticker in tickers:
  input_file = '%s/%s' % (raw_dir, ticker)
  with open(input_file, 'r') as fp:
    lines = fp.read().splitlines()
  min_date = '9999-99'
  max_date = '0000-00'
  for line in lines:
    items = line.split(',')
    assert len(items) == 14
    date = items[1]
    y, m, d = date.split('-')
    date = '%s-%s' % (y, m)
    min_date = min(min_date, date)
    max_date = max(max_date, date)
  date = min_date
  while date <= max_date:
    updateDistr(distr, date)
    date = getNextDate(date)
  print '%s: %d entries' % (ticker, len(lines))

min_date = min(distr.keys())
max_date = max(distr.keys())
print 'min date: %s' % min_date
print 'max date: %s' % max_date

with open(distr_file, 'w') as fp:
  print >> fp, 'date\tcount'
  date = min_date
  while date <= max_date:
    print >> fp, '%s\t%d' % (date, distr.get(date, 0))
    date = getNextDate(date)

