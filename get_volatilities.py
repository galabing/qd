#!/usr/bin/python

""" Computes volatilities for all stocks of all time.

    Example usage:
      ./get_volatilities.py --price_dir=./prices
                            --k=24
                            --volatility_dir=./volatilities24
      or
      ./get_volatilities.py --price_dir=./prices
                            --k=12
                            --future
                            --volatility_dir=./fvolatilities24

    It assumes no holes in price history (ie, current row - k
    should correspond to price k months ago).  This should be close
    enough for practical purposes (only being used as validation,
    not features).
"""

import argparse
import logging
import math
import os
import utils

EPS = 0.01  # to prevent divide-by-zero in calculating gains

def readPrices(price_file):
  with open(price_file, 'r') as fp:
    lines = fp.read().splitlines()
  prices = []  # [[ymd, price] ...]
  prev_ymd = None
  for line in lines:
    ymd, price = line.split('\t')
    if prev_ymd is not None:
      assert ymd > prev_ymd
    prev_ymd = ymd
    prices.append([ymd, float(price)])
  return prices

def getMonthlyGains(prices):
  gains = []  # [[ymd, gain] ...]
  for i in range(1, len(prices)):
    gains.append([prices[i][0],
                  (prices[i][1] - prices[i-1][1]) / (prices[i-1][1] + EPS)])
  return gains

def computeStd(values):
  mean = sum(values) / len(values)
  std = 0.0
  for value in values:
    std += (value - mean)**2
  std /= len(values)
  return math.sqrt(std)

def getVolatilities(price_dir, k, volatility_dir, future):
  tickers = sorted(os.listdir(price_dir))
  logging.info('processing %d tickers' % len(tickers))
  for ticker in tickers:
    logging.info(ticker)
    prices = readPrices('%s/%s' % (price_dir, ticker))
    gains = getMonthlyGains(prices)
    with open('%s/%s' % (volatility_dir, ticker), 'w') as fp:
      if future:
        for i in range(len(gains)-k+1):
          print >> fp, '%s\t%f' % (prices[i][0],
              computeStd([gains[j][1] for j in range(i, i+k)]))
      else:
        for i in range(k-1, len(gains)):
          print >> fp, '%s\t%f' % (gains[i][0],
              computeStd([gains[j][1] for j in range(i-k+1, i+1)]))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--price_dir', required=True)
  parser.add_argument('--k', type=int, required=True,
                      help='number of months to look for volatility')
  parser.add_argument('--volatility_dir', required=True)
  parser.add_argument('--future', action='store_true')
  args = parser.parse_args()
  utils.configLogging()
  # Sanity checks.
  assert args.k > 1, 'k must be positive'
  assert args.volatility_dir.endswith(str(args.k)), (
      'volatility_dir should be suffixed by k for safety')
  getVolatilities(args.price_dir, args.k, args.volatility_dir, args.future)

if __name__ == '__main__':
  main()

