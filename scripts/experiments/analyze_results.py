#!/usr/bin/python

""" Analyzes simulation results.
"""

input_dir = '/Users/lnyang/lab/qd/data/experiments/Q/results'
version = -1
delay = 0
output_dir = '%s/misc' % input_dir

months = 12

# max number of top stocks to look
max_look = -1
# max number of top stocks to trade
max_pick = 3
# max number of holdings per stock
max_hold = 10

output_file = '%s/l%d_p%d_h%d.tsv' % (output_dir, max_look, max_pick, max_hold)

def readResults(input_file):
  with open(input_file, 'r') as fp:
    lines = fp.read().splitlines()
  results = dict()
  i = 0
  DATE_PREFIX = 'date: '
  while i < len(lines):
    if not lines[i].startswith(DATE_PREFIX):
      i += 1
      continue
    date = lines[i][len(DATE_PREFIX):]
    assert date not in results
    results[date] = []  # [[ticker, gain, score] ...]
    j = i + 1
    while j < len(lines):
      if lines[j].startswith(DATE_PREFIX):
        break
      tmp, ticker, gain, score = lines[j].split('\t')
      assert tmp == ''
      gain = float(gain)
      score = float(score)
      if len(results[date]) > 0:
        assert results[date][-1][2] >= score
      results[date].append([ticker, gain, score])
      j += 1
    i = j
  return results

def getSaleDate(buy_date, months):
  year, month = buy_date.split('-')
  year = int(year)
  month = int(month)
  year += int(months / 12)
  month += months % 12
  if month > 12:
    year += 1
    month -= 12
  return '%04d-%02d' % (year, month)

def update(date, items, months, max_look, max_pick, max_hold, buys, record):
  tickers = [item[0] for item in record if item[2] > date]
  holds = dict()  # ticker => num holdings
  for ticker in tickers:
    if ticker not in holds:
      holds[ticker] = 1
    else:
      holds[ticker] += 1
  i, j = 0, 0
  trans = []
  while i < max_pick and (max_look < 0 or j < max_look):
    ticker, gain, score = items[j]
    if ticker in holds and max_hold > 0 and holds[ticker] >= max_hold:
      j += 1
      continue
    trans.append([ticker, gain, score])
    record.append([ticker, date, getSaleDate(date, months)])
    i += 1
    j += 1
  assert date not in buys
  buys[date] = trans

results = readResults('%s/version_%d_delay_%d' % (input_dir, version, delay))
print '%d result dates' % len(results)

buys = dict()  # date => [[ticker, gain, score], ...]
record = []  # [[ticker, buy_date, sale_date], ...]

for date in sorted(results.keys()):
  items = results[date]
  update(date, items, months, max_look, max_pick, max_hold, buys, record)

with open(output_file, 'w') as fp:
  print >> fp, '\t'.join(['date', 'buys', 'total_hold', 'max_hold', 'mh_ticker', 'gain'])
  for date in sorted(buys.keys()):
    trans = buys[date]
    gain = sum([t[1] for t in trans])/len(trans)
    hold = [item[0] for item in record if item[1] <= date and item[2] > date]
    count = dict()  # ticker => count
    for ticker in hold:
      if ticker not in count:
        count[ticker] = 1
      else:
        count[ticker] += 1
    max_hold = 0
    mh_ticker = None
    for ticker, c in count.iteritems():
      if c > max_hold:
        max_hold = c
        mh_ticker = ticker
    print >> fp, '\t'.join([date, str(len(trans)), str(len(hold)), str(max_hold), mh_ticker, '%.2f%%' % (gain*100)])

