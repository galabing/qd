#!/usr/bin/python

""" Classifies tickers into sector groups.
    Post processing: grouped sectors '', 'N/A', 'None' into 'Unknown'.
"""

input_file = '/Users/lnyang/lab/qd/data/tickers'
info_file = '/Users/lnyang/lab/qd/data/sf1_ticker_info.txt'

output_dir = '/Users/lnyang/lab/qd/data/ticker_groups/sectors'

with open(input_file, 'r') as fp:
  tickers = fp.read().splitlines()

with open(info_file, 'r') as fp:
  lines = fp.read().splitlines()

assert len(lines) > 0
headers = lines[0].split('\t')
assert headers[0] == 'Ticker'
assert headers[5] == 'Sector'

ticker_sector = dict()
for i in range(1, len(lines)):
  items = lines[i].split('\t')
  ticker_sector[items[0]] = items[5].replace('/', '-').replace(' ', '-')

fp_dict = dict()
for sector in set(ticker_sector.values()):
  fp_dict[sector] = open('%s/sector_%s' % (output_dir, sector), 'w')

for ticker in tickers:
  print >> fp_dict[ticker_sector.get(ticker, '')], ticker

for fp in fp_dict.itervalues():
  fp.close()

