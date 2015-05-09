#!/usr/bin/python

""" Computes log of any basic feature from any dimension file.

    Example usage:
      ./compute_log_feature.py --l1_dir=./l1
                               --ticker_file=./tickers
                               --dimension=ARQ
                               --header=CAPEX
                               --negate
                               --feature_dir=./CAPEX-ARQ
                               --info_file=./CAPEX-ARQ/info
"""

import argparse
import logging
import math
import os
import utils

def computeLogFeature(l1_dir, ticker_file, dimension, header,
                      negate, feature_dir, info_file=None):
  tickers = utils.readTickers(ticker_file)
  logging.info('processing %d tickers' % len(tickers))
  features = []
  for ticker in tickers:
    logging.info(ticker)
    dimension_file = '%s/%s/%s.tsv' % (l1_dir, ticker, dimension)
    dfeatures = utils.readL1Column(dimension_file, header)
    if dfeatures is None:
      continue
    with open('%s/%s' % (feature_dir, ticker), 'w') as fp:
      for date, feature in dfeatures:
        if feature is None:
          features.append((utils.getY(date), feature))
          continue
        if negate:
          feature = -feature
        if feature <= 0:
          features.append((utils.getY(date), None))
          continue
        feature = math.log(feature)
        print >> fp, '%s\t%f' % (date, feature)
        features.append((utils.getY(date), feature))
  if info_file is not None:
    utils.writeFeatureInfo(
        [l1_dir, ticker_file, dimension, header, negate, feature_dir],
        features, info_file)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--l1_dir', required=True)
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--dimension', required=True)
  parser.add_argument('--header', required=True)
  parser.add_argument('--negate', action='store_true',
                      help='negate the feature (eg, CAPEX)')
  parser.add_argument('--feature_dir', required=True)
  parser.add_argument('--info_file')
  args = parser.parse_args()
  utils.configLogging()
  computeLogFeature(args.l1_dir, args.ticker_file, args.dimension,
                    args.header, args.negate, args.feature_dir,
                      args.info_file)

if __name__ == '__main__':
  main()

