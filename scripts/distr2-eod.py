#!/usr/bin/python

""" Computes several distributions for EOD:
    - start month => #tickers
    - end month => #tickers
    - duration (months) => #tickers
    - missing months => #tickers
    First available adj close price is used for each month.
"""

import os

raw_dir = '/Users/lnyang/lab/qd/data/eod/raw'
misc_dir = '/Users/lnyang/lab/qd/data/eod/misc'

def writeDistr(distr, suffix, label):
  with open('%s/distr2%s.tsv' % (misc_dir, suffix), 'w') as fp:
    print >> fp, '%s\tcount' % label
    for key in sorted(distr.keys()):
      count = distr[key]
      print >> fp, '%s\t%d' % (str(key), count)

def getDate(date):
  y, m, d = date.split('-')
  return '%s-%s' % (y, m)

def getNextMonth(date):
  y, m = date.split('-')
  y = int(y)
  m = int(m)
  assert m >= 1
  assert m <= 12
  if m < 12:
    m += 1
  else:
    y += 1
    m = 1
  return '%04d-%02d' % (y, m)

def getDuration(min_date, max_date):
  date = min_date
  count = 0
  while date <= max_date:
    count += 1
    date = getNextMonth(date)
  return count

def updateDistr(distr, key):
  if key not in distr: distr[key] = 1
  else: distr[key] += 1

tickers = sorted(os.listdir(raw_dir))
print 'processing %d tickers' % len(tickers)

start_distr = dict()
end_distr = dict()
duration_distr = dict()
missing_distr = dict()

for ticker in tickers:
  with open('%s/%s' % (raw_dir, ticker), 'r') as fp:
    lines = fp.read().splitlines()
  min_date = '9999-99'
  max_date = '0000-00'
  dates = set()
  prev_date = None
  for line in lines:
    items = line.split(',')
    assert len(items) == 14
    date = items[1]
    adj_close = items[-1]
    if date == '' or adj_close == '':
      continue
    date = getDate(date)
    if date == prev_date:
      continue
    min_date = min(min_date, date)
    max_date = max(max_date, date)
    dates.add(date)
    prev_date = date
  duration = getDuration(min_date, max_date)
  missing = duration - len(dates)
  assert missing >= 0, 'debug %s: %s, %s, %d, %d, %s' % (ticker, min_date, max_date, duration, missing, sorted(dates))
  updateDistr(start_distr, min_date)
  updateDistr(end_distr, max_date)
  updateDistr(duration_distr, duration)
  updateDistr(missing_distr, missing)
  print '%s: %d dates' % (ticker, len(dates))

writeDistr(start_distr, '-start', 'start_month')
writeDistr(end_distr, '-end', 'end_month')
writeDistr(duration_distr, '-duration', 'duration_m')
writeDistr(missing_distr, '-missing', 'missing_m')

