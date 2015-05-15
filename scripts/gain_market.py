#!/usr/bin/python

""" Compares avg gain to market (see surviver bias).
"""

data_dir = '/Users/lnyang/lab/qd/data'

min_price = 10
window = 1
market = 'R3000'

gain_dir = '%s/gains%d/%d' % (data_dir, min_price, window)

ticker_file = '%s/tickers' % data_dir
market_file = '%s/yahoo/%s/gains/%d/%s' % (data_dir, market, window, market)

min_date = '2004-01-01'
max_date = '9999-99-99'

output_file = '%s/misc/gains%d_%d_%s.tsv' % (
    data_dir, min_price, window, market)

with open(ticker_file, 'r') as fp:
  tickers = sorted(fp.read().splitlines())
print 'processing %d tickers' % len(tickers)

data_dict = dict()  # ym => [gain, ...]
market_dict = dict()  # ym => gain

for ticker in tickers:
  gain_file = '%s/%s' % (gain_dir, ticker)
  with open(gain_file, 'r') as fp:
    lines = fp.read().splitlines()
  for line in lines:
    date, gain = line.split('\t')
    if date < min_date: continue
    if date > max_date: continue
    y, m, d = date.split('-')
    ym = '%s-%s' % (y, m)
    gain = float(gain)
    if ym not in data_dict:
      data_dict[ym] = [gain]
    else:
      data_dict[ym].append(gain)

with open(market_file, 'r') as fp:
  lines = fp.read().splitlines()
for line in lines:
  date, gain = line.split('\t')
  if date < min_date: continue
  if date > max_date: continue
  y, m, d = date.split('-')
  ym = '%s-%s' % (y, m)
  gain = float(gain)
  assert ym not in market_dict, 'dup key %s' % ym
  market_dict[ym] = gain

dates = sorted(data_dict.keys())
print 'processed %d dates' % len(dates)

with open(output_file, 'w') as fp:
  print >> fp, 'date\tavg\tmarket\tcount'
  for date in dates:
    data_gains = data_dict[date]
    num_gains = len(data_gains)
    avg_gain = sum(data_gains)/num_gains
    market_gain = market_dict[date]
    print >> fp, '%s\t%f\t%f\t%d' % (date, avg_gain, market_gain, num_gains)

