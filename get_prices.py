#!/usr/bin/python

""" Collects (adj) close data.

    Example usage:
      ./get_prices.py --eod_dir=./eod/raw
                      --ticker_file=./tickers
                      --price_dir=./eod/prices
                      --use_raw

    Valid (adj) close from first trading day of each month is collected
    for each ticker.

    Test: spot checked a few entries for AAPL, comparing with raw data.
"""

import argparse
import logging
import utils

def getPrices(eod_dir, ticker_file, use_raw, price_dir):
  tickers = utils.readTickers(ticker_file)
  logging.info('processing %d tickers' % len(tickers))

  for ticker in tickers:
    with open('%s/%s' % (eod_dir, ticker), 'r') as fp:
      lines = fp.read().splitlines()
    prev_date = None
    count = 0
    with open('%s/%s' % (price_dir, ticker), 'w') as fp:
      for line in lines:
        items = line.split(',')
        assert len(items) == 14
        date = items[1]
        if use_raw:
          close = items[5]
        else:
          close = items[-2]
        if date == '' or close == '':
          continue
        date = utils.getYm(date)
        if date == prev_date:
          continue
        prev_date = date
        print >> fp, '%s\t%s' % (items[1], close)
        count += 1
    logging.info('%s: %d prices' % (ticker, count))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--eod_dir', required=True)
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--price_dir', required=True)
  parser.add_argument('--use_raw', action='store_true',
                      help='use raw instead of adj close')
  args = parser.parse_args()
  utils.configLogging()
  getPrices(args.eod_dir, args.ticker_file, args.use_raw, args.price_dir)

if __name__ == '__main__':
  main()

