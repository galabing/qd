#!/usr/bin/python

""" Computes any basic feature from any dimension file.

    Example usage:
      ./compute_basic_feature.py --l1_dir=./l1
                                 --ticker_file=./tickers
                                 --dimension=ART
                                 --header=PE
                                 --invert
                                 --feature_dir=./ep
                                 --info_file=./ep/info
"""

import argparse
import logging
import os
import utils

def computeBasicFeature(l1_dir, ticker_file, dimension, header,
                        invert, feature_dir, info_file=None):
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
        if feature is None or (invert and feature == 0):
          features.append((utils.getY(date), feature))
          continue
        if invert:
          feature = 1.0/feature
        print >> fp, '%s\t%f' % (date, feature)
        features.append((utils.getY(date), feature))
  if info_file is not None:
    utils.writeFeatureInfo(
        [l1_dir, ticker_file, dimension, header, invert, feature_dir],
        features, info_file)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--l1_dir', required=True)
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--dimension', required=True)
  parser.add_argument('--header', required=True)
  parser.add_argument('--invert', action='store_true',
                      help='invert the feature (eg, PE to EP)')
  parser.add_argument('--feature_dir', required=True)
  parser.add_argument('--info_file')
  args = parser.parse_args()
  utils.configLogging()
  computeBasicFeature(args.l1_dir, args.ticker_file, args.dimension,
                      args.header, args.invert, args.feature_dir,
                      args.info_file)

if __name__ == '__main__':
  main()

