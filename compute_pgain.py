#!/usr/bin/python

""" Computes previous gains.  This simply takes dated gains and reindex the
    gains by the end date so that it can be used as a feature.  Eg, in a
    6-month gain file, a row could be:
      2000-01-01 0.1
    meaning the gain 6 months from 2000-01-01 is 10%.  This will be converted
    to:
      2000-07-01 0.1
    meaning the past 6-month gain ending on 2000-07-01 is 10%.

    Example usage:
      ./compute_pgain.py --gain_dir=./gains/6
                         --k=6
                         --ticker_file=./tickers
                         --pgain_dir=./pgain/6
"""

import argparse
import logging
import os
import utils

def computePgain(gain_dir, k, ticker_file, pgain_dir):
  tickers = utils.readTickers(ticker_file)
  logging.info('processing %d tickers' % len(tickers))

  for ticker in tickers:
    logging.info(ticker)
    gain_file = '%s/%s' % (gain_dir, ticker)
    if not os.path.isfile(gain_file):
      logging.info('gain file does not exist: %s' % gain_file)
      continue
    dgains = utils.readKeyValueFile(gain_file)
    with open('%s/%s' % (pgain_dir, ticker), 'w') as fp:
      for date, gain in dgains:
        ym = utils.getYm(date)
        pdate = utils.getNextYm(ym, k)
        print >> fp, '%s-01\t%f' % (pdate, gain)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--gain_dir', required=True)
  parser.add_argument('--k', type=int,
                      help='number of months in computing gain')
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--pgain_dir', required=True)
  args = parser.parse_args()
  assert args.gain_dir.endswith(str(args.k))
  assert args.pgain_dir.endswith(str(args.k))
  utils.configLogging()
  computePgain(args.gain_dir, args.k, args.ticker_file, args.pgain_dir)

if __name__ == '__main__':
  main()

