#!/usr/bin/python

""" Computes EBIT/EV from ART, which is just inverse of EVEBIT.

    Example usage:
      ./compute_ebitev.py --l1_dir=./l1
                          --ticker_file=./tickers
                          --ebitev_dir=./ebitev
"""

import argparse
import logging
import os
import utils

DIMENSION = 'ART'
EVEBIT_HEADER = 'EVEBIT'

def computeEbitev(l1_dir, ticker_file, ebitev_dir, stats_file=None):
  tickers = utils.readTickers(ticker_file)
  logging.info('processing %d tickers' % len(tickers))
  features = []
  for ticker in tickers:
    logging.info(ticker)
    dimension_file = '%s/%s/%s.tsv' % (l1_dir, ticker, DIMENSION)
    if not os.path.isfile(dimension_file):
      logging.warning('dimension file does not exist: %s' % dimension_file)
      continue
    devebits = utils.readL1Column(dimension_file, EVEBIT_HEADER)
    with open('%s/%s' % (ebitev_dir, ticker), 'w') as fp:
      for date, evebit in devebits:
        if evebit is not None and evebit != 0:
          ebitev = 1/evebit
          print >> fp, '%s\t%f' % (date, ebitev)
          features.append((utils.getY(date), ebitev))
        else:
          features.append((utils.getY(date), None))
  if stats_file is not None:
    utils.writeFeatureStats(features, stats_file)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--l1_dir', required=True)
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--ebitev_dir', required=True)
  parser.add_argument('--stats_file')
  args = parser.parse_args()
  utils.configLogging()
  computeEbitev(args.l1_dir, args.ticker_file, args.ebitev_dir,
                args.stats_file)

if __name__ == '__main__':
  main()

