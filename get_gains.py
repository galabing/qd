#!/usr/bin/python

""" Computes gains for all stocks of all time.

    Example usage:
      ./get_gains.py --price_dir=./prices
                     --k=12
                     --gain_dir=./gains12

    Can optionally provide --min_raw_price and --max_raw_price to only compute
    gains whose current raw price is in range.  In this case --raw_price_dir
    is also required.

    Gain = (adj_price_in_k_mon - current_adj_price) / (current_adj_price + eps)

    Test: spot checked a few entries for AAPL.
"""

import argparse
import logging
import os
import utils

MIN_RAW_PRICE = float('-Inf')
MAX_RAW_PRICE = float('Inf')
EPS = 0.01

def readPrices(price_file):
  with open(price_file, 'r') as fp:
    lines = fp.read().splitlines()
  prices = dict()  # ym => [ymd, price]
  for line in lines:
    ymd, price = line.split('\t')
    ym = utils.getYm(ymd)
    assert ym not in prices
    prices[ym] = [ymd, float(price)]
  return prices

def getGains(price_dir, k, min_raw_price, max_raw_price, raw_price_dir,
             gain_dir):
  tickers = sorted(os.listdir(price_dir))
  logging.info('processing %d tickers' % len(tickers))
  skip_stats = {
      'ym2': 0,
      'raw': 0,
      'min_raw_price': 0,
      'max_raw_price': 0,
  }
  total = 0
  for ticker in tickers:
    logging.info(ticker)
    prices = readPrices('%s/%s' % (price_dir, ticker))
    if raw_price_dir:
      raw_prices = readPrices('%s/%s' % (raw_price_dir, ticker))
    with open('%s/%s' % (gain_dir, ticker), 'w') as fp:
      for ym in sorted(prices.keys()):
        ym2 = utils.getNextYm(ym, k)
        if ym2 not in prices:
          skip_stats['ym2'] += 1
          continue
        ymd, price = prices[ym]
        ymd2, price2 = prices[ym2]
        assert price >= 0
        assert price2 >= 0
        if min_raw_price > MIN_RAW_PRICE or max_raw_price < MAX_RAW_PRICE:
          if ym not in raw_prices:
            skip_stats['raw'] += 1
            continue
          raw_price = raw_prices[ym][1]
          if raw_price < min_raw_price:
            skip_stats['min_raw_price'] += 1
            continue
          if raw_price > max_raw_price:
            skip_stats['max_raw_price'] += 1
            continue
        gain = (price2 - price) / (price + EPS)
        print >> fp, '%s\t%f' % (ymd, gain)
        total += 1
  logging.info('skip_stats: %s' % skip_stats)
  logging.info('write %d data points' % total)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--price_dir', required=True)
  parser.add_argument('--k', type=int, required=True,
                      help='number of months to look for gain')
  parser.add_argument('--min_raw_price', type=float, default=MIN_RAW_PRICE)
  parser.add_argument('--max_raw_price', type=float, default=MAX_RAW_PRICE)
  parser.add_argument('--raw_price_dir',
                      help='raw price dir, required if min_raw_price or '
                           'max_raw_price is specified')
  parser.add_argument('--gain_dir', required=True)
  args = parser.parse_args()
  utils.configLogging()
  # Sanity checks.
  assert args.gain_dir.endswith(str(args.k)), (
      'gain_dir should be suffixed by k for safety')
  assert args.min_raw_price < args.max_raw_price, (
      'min_raw_price >= max_raw_price: %f vs %f' % (
      args.min_raw_price, args.max_raw_price))
  if args.min_raw_price > MIN_RAW_PRICE or args.max_raw_price < MAX_RAW_PRICE:
    assert args.raw_price_dir, 'must specify --raw_price_dir'
  getGains(args.price_dir, args.k, args.min_raw_price, args.max_raw_price,
           args.raw_price_dir, args.gain_dir)

if __name__ == '__main__':
  main()

