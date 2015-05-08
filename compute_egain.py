#!/usr/bin/python

""" Computes excess gains.

    Example usage:
      ./compute_egain.py --gain_dir=./gains/6
                         --ticker_file=./tickers
                         --market_file=./sp500/6
                         --egain_dir=./egain/6
"""

import argparse
import logging
import os
import utils

# ym => [ymd, gain]
def getGainDict(gain_file):
  dgains = utils.readKeyValueFile(gain_file)
  gain_dict = dict()
  for date, gain in dgains:
    ym = utils.getYm(date)
    assert ym not in gain_dict
    gain_dict[ym] = [date, gain]
  return gain_dict

def computeEgain(gain_dir, ticker_file, market_file, egain_dir):
  tickers = utils.readTickers(ticker_file)
  logging.info('processing %d tickers' % len(tickers))

  market_dict = getGainDict(market_file)

  missing = 0
  for ticker in tickers:
    logging.info(ticker)
    gain_file = '%s/%s' % (gain_dir, ticker)
    if not os.path.isfile(gain_file):
      logging.info('gain file does not exist: %s' % gain_file)
      continue
    ticker_dict = getGainDict(gain_file)
    with open('%s/%s' % (egain_dir, ticker), 'w') as fp:
      for ym in sorted(ticker_dict.keys()):
        if ym in market_dict:
          date, ticker_gain = ticker_dict[ym]
          tmp, market_gain = market_dict[ym]
          print >> fp, '%s\t%f' % (date, ticker_gain - market_gain)
        else:
          missing += 1
  logging.info('%d missing dates from market' % missing)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--gain_dir', required=True)
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--market_file', required=True)
  parser.add_argument('--egain_dir', required=True)
  args = parser.parse_args()
  utils.configLogging()
  computeEgain(args.gain_dir, args.ticker_file, args.market_file,
               args.egain_dir)

if __name__ == '__main__':
  main()

