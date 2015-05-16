#!/usr/bin/python

""" Computes previous features.  This simply takes dated features and reindex
    them by the end date so that it can be used as a feature.  Eg, in a
    6-month gain file, a row could be:
      2000-01-01 0.1
    meaning the gain 6 months from 2000-01-01 is 10%.  This will be converted
    to:
      2000-07-01 0.1
    meaning the past 6-month gain ending on 2000-07-01 is 10%.

    Example usage:
      ./compute_previou_feature.py --feature_dir=./gains/6
                                   --k=6
                                   --ticker_file=./tickers
                                   --pfeature_dir=./pgain/6
"""

import argparse
import logging
import os
import utils

def computePreviousFeature(feature_dir, k, ticker_file, pfeature_dir):
  tickers = utils.readTickers(ticker_file)
  logging.info('processing %d tickers' % len(tickers))

  for ticker in tickers:
    logging.info(ticker)
    feature_file = '%s/%s' % (feature_dir, ticker)
    if not os.path.isfile(feature_file):
      logging.info('feature file does not exist: %s' % feature_file)
      continue
    dfeatures = utils.readKeyValueFile(feature_file)
    with open('%s/%s' % (pfeature_dir, ticker), 'w') as fp:
      for date, feature in dfeatures:
        ym = utils.getYm(date)
        pdate = utils.getNextYm(ym, k)
        print >> fp, '%s-01\t%f' % (pdate, feature)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--feature_dir', required=True)
  parser.add_argument('--k', type=int,
                      help='number of months in computing feature')
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--pfeature_dir', required=True)
  args = parser.parse_args()
  utils.configLogging()
  computePreviousFeature(args.feature_dir, args.k, args.ticker_file,
                         args.pfeature_dir)

if __name__ == '__main__':
  main()

