#!/usr/bin/python

""" Compares ARQ and MRQ data.
"""

import datetime
import os

def readL1(l1_file):
  with open(l1_file, 'r') as fp:
    lines = fp.read().splitlines()
  assert len(lines) > 0
  headers = lines[0].split('\t')
  assert len(headers) > 0
  assert headers[0] == 'date'
  # date => { indicator => value }
  l1 = dict()
  for i in range(1, len(lines)):
    items = lines[i].split('\t')
    indicator_dict = dict()
    for j in range(1, len(items)):
      if items[j] == '':
        continue
      indicator_dict[headers[j]] = items[j]
    l1[items[0]] = indicator_dict
  return l1

def updateStats(stats, indicator, reported, modified, smodified):
  if indicator not in stats:
    stats[indicator] = [reported, modified, smodified]
  else:
    stats[indicator][0] += reported
    stats[indicator][1] += modified
    stats[indicator][2] += smodified

l1_dir = '/Users/lnyang/lab/qd/data/sf1/l1'
# Modifications above this threshold are considered significant.
sthreshold = 0.1
debug_tickers = None  #['AAPL']

if debug_tickers is not None:
  tickers = debug_tickers
else:
  tickers = sorted(os.listdir(l1_dir))
print 'processing %d tickers' % len(tickers)

# indicator => (#reported, #modified)
stats = dict()
for ticker in tickers:
  ticker_dir = '%s/%s' % (l1_dir, ticker)
  nd_file = '%s/ND.tsv' % ticker_dir
  if not os.path.isfile(nd_file):
    print 'nd file missing: %s' % nd_file
    continue
  nd = readL1(nd_file)
  # Collect arq, mrq date pairs.
  # In ND, the 'date' column corresponds to filing date of arq,
  # while the 'FILINGDATE' column corresponds to the report period of mrq.
  arq_mrq_dates = []
  for arq_date, indicator_dict in nd.iteritems():
    mrq_date = indicator_dict.get('FILINGDATE', '')
    if mrq_date == '':
      continue
    assert mrq_date.endswith('.0')
    try:
      mrq_date = datetime.datetime.strptime(
          mrq_date[:-2], '%Y%m%d').strftime('%Y-%m-%d')
    except ValueError:
      print 'error in parsing date: %s, %s' % (ticker, mrq_date)
      continue
    arq_mrq_dates.append([arq_date, mrq_date])

  arq_file = '%s/ARQ.tsv' % ticker_dir
  mrq_file = '%s/MRQ.tsv' % ticker_dir
  if not os.path.isfile(arq_file):
    print 'arq file missing: %s' % arq_file
    continue
  if not os.path.isfile(mrq_file):
    print 'mrq file missing: %s' % mrq_file
    continue
  arq = readL1(arq_file)
  mrq = readL1(mrq_file)

  for arq_date, mrq_date in arq_mrq_dates:
    arq_dict = arq.get(arq_date, None)
    mrq_dict = mrq.get(mrq_date, None)
    if arq_dict is None or mrq_dict is None:
      continue

    for indicator, arq_value in arq_dict.iteritems():
      modified = 0
      smodified = 0
      mrq_value = mrq_dict.get(indicator, None)
      if mrq_value is None:
        smodified = 1
      elif arq_value != mrq_value:
        arq_value = float(arq_value)
        mrq_value = float(mrq_value)
        if abs(mrq_value - arq_value) / (abs(arq_value) + 1e-5) > sthreshold:
          smodified = 1
        else:
          modified = 1
      #print 'debug: [%s, %s, %s] %s: %s => %s' % (
          #ticker, arq_date, mrq_date, indicator, arq_value, mrq_value)
      updateStats(stats, indicator, 1, modified, smodified)
    for indicator in mrq_dict.iterkeys():
      if indicator not in arq_dict:
        #print 'debug: [%s, %s, %s] %s: %s => %s' % (
        #    ticker, arq_date, mrq_date, indicator, None, mrq_value)
        updateStats(stats, indicator, 1, 0, 1)

stats = [[indicator, v[0], v[1], v[2], float(v[1])/v[0], float(v[2])/v[0]]
         for indicator, v in stats.iteritems()]
stats.sort(key=lambda item: item[4], reverse=True)
for indicator, reported, modified, smodified, rate, srate in stats:
  print '%s: %d rep, %d mod, %d smod, mod_perc: %.2f%%, smod_perc: %.2f%%' % (
      indicator, reported, modified, smodified, rate*100, srate*100)

