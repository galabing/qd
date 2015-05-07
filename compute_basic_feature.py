#!/usr/bin/python

""" Computes any basic feature from any dimension file.

    Example usage:
      ./compute_basic_feature.py --l1_dir=./l1
                                 --ticker_file=./tickers
                                 --dimension=ART
                                 --header=PE
                                 --feature_dir=./pe
                                 --stats_file=./pe/stats.tsv
"""

import argparse
import logging
import os
import utils

def computeBasicFeature(l1_dir, ticker_file, dimension, header,
                        feature_dir, stats_file=None):
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
        if feature is not None:
          print >> fp, '%s\t%f' % (date, feature)
          features.append((utils.getY(date), feature))
        else:
          features.append((utils.getY(date), None))
  if stats_file is not None:
    utils.writeFeatureStats(features, stats_file)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--l1_dir', required=True)
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--dimension', required=True)
  parser.add_argument('--header', required=True)
  parser.add_argument('--feature_dir', required=True)
  parser.add_argument('--stats_file')
  args = parser.parse_args()
  utils.configLogging()
  computeEbitev(args.l1_dir, args.ticker_file, args.dimension, args.header,
                args.feature_dir, args.stats_file)

if __name__ == '__main__':
  main()

