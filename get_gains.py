#!/usr/bin/python

""" Computes gains for all stocks of all time.

    Example usage:
      ./get_gains.py --price_dir=./prices
                     --k=12
                     --gain_dir=./gains12

    Gain = (price_in_k_mon - current_price) / (current_price + eps)

    Test: spot checked a few entries for AAPL.
"""

import argparse
import logging
import os
import utils

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

def getGains(price_dir, k, gain_dir):
  tickers = sorted(os.listdir(price_dir))
  logging.info('processing %d tickers' % len(tickers))
  for ticker in tickers:
    logging.info(ticker)
    prices = readPrices('%s/%s' % (price_dir, ticker))
    with open('%s/%s' % (gain_dir, ticker), 'w') as fp:
      for ym in sorted(prices.keys()):
        ym2 = utils.getNextYm(ym, k)
        if ym2 not in prices:
          continue
        ymd, price = prices[ym]
        ymd2, price2 = prices[ym2]
        assert price >= 0
        assert price2 >= 0
        gain = (price2 - price) / (price + EPS)
        print >> fp, '%s\t%f' % (ymd, gain)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--price_dir', required=True)
  parser.add_argument('--k', type=int, required=True,
                      help='number of months to look for gain')
  parser.add_argument('--gain_dir', required=True)
  args = parser.parse_args()
  utils.configLogging()
  # Sanity check.
  assert args.gain_dir.endswith(str(args.k)), (
      'gain_dir should be suffixed by k for safety')
  getGains(args.price_dir, args.k, args.gain_dir)

if __name__ == '__main__':
  main()

