#!/usr/bin/python

""" Collects some feature/gain data points for plotting, with each line being
    <ticker> <feature_date> <feature> <gain_date> <gain> (tab delimited).

    Example usage:
      ./get_feature_gain.py --feature_dir=./ebitev
                            --gain_dir=./gains12
                            --ticker_file=./tickers
                            --min_date=2004-01-01
                            --max_date=2009-12-31
                            --window=60
                            --min_feature_perc=0.01
                            --max_feature_perc=0.99
                            --min_gain=-1
                            --max_gain=1
                            --output_file=./ebitev-12
"""

import argparse
import bisect
import datetime
import logging
import os
import utils

def getDelta(early_date, late_date):
  early = datetime.datetime.strptime(early_date, '%Y-%m-%d')
  late = datetime.datetime.strptime(late_date, '%Y-%m-%d')
  assert early <= late
  return (late - early).days

def getFeatureGain(feature_dir, gain_dir, ticker_file, min_date, max_date,
                   window, min_feature_perc, max_feature_perc, min_gain,
                   max_gain, output_file):
  tickers = utils.readTickers(ticker_file)
  logging.info('processing %d tickers' % len(tickers))

  skip_stats = {'feature_file': 0,
                'gain_file': 0,
                'gain_index': 0,
                'window': 0,
                'min_date': 0,
                'max_date': 0,
                'min_gain': 0,
                'max_gain': 0,
                'min_feature_perc': 0,
                'max_feature_perc': 0}

  data = []  # [[ticker, feature_date, feature, gain_date, gain] ...]
  for ticker in tickers:
    logging.info(ticker)
    feature_file = '%s/%s' % (feature_dir, ticker)
    gain_file = '%s/%s' % (gain_dir, ticker)
    if not os.path.isfile(feature_file):
      skip_stats['feature_file'] += 1
      continue
    if not os.path.isfile(gain_file):
      skip_stats['gain_file'] += 1
      continue
    dfeatures = utils.readKeyValueFile(feature_file)
    dgains = utils.readKeyValueFile(gain_file)
    gain_dates = [dgain[0] for dgain in dgains]
    for dfeature in dfeatures:
      feature_date, feature = dfeature
      gain_index = bisect.bisect_left(gain_dates, feature_date)
      if gain_index >= len(dgains):
        skip_stats['gain_index'] += 1
        continue
      gain_date, gain = dgains[gain_index]
      delta = getDelta(feature_date, gain_date)
      if delta > window:
        skip_stats['window'] += 1
        continue
      if gain_date < min_date:
        skip_stats['min_date'] += 1
        continue
      if gain_date > max_date:
        skip_stats['max_date'] += 1
        continue
      if gain < min_gain:
        skip_stats['min_gain'] += 1
        continue
      if gain > max_gain:
        skip_stats['max_gain'] += 1
        continue
      data.append([ticker, feature_date, feature, gain_date, gain])

  features = sorted([item[2] for item in data])
  min_feature = features[int(len(features) * min_feature_perc)]
  max_feature = features[int(len(features) * max_feature_perc)]
  logging.info('min_feature: %f' % min_feature)
  logging.info('max_feature: %f' % max_feature)

  with open(output_file, 'w') as fp:
    for ticker, feature_date, feature, gain_date, gain in data:
      if feature < min_feature:
        skip_stats['min_feature_perc'] += 1
        continue
      if feature > max_feature:
        skip_stats['max_feature_perc'] += 1
        continue
      print >> fp, '\t'.join([
          ticker, feature_date, '%.6f' % feature, gain_date, '%.6f' % gain])

  logging.info('skip_stats: %s' % skip_stats)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--feature_dir', required=True)
  parser.add_argument('--gain_dir', required=True)
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--min_date', default='0000-00-00')
  parser.add_argument('--max_date', default='9999-99-99')
  parser.add_argument('--window', type=int, default=60)
  parser.add_argument('--min_feature_perc', type=float, default=0.01)
  parser.add_argument('--max_feature_perc', type=float, default=0.99)
  parser.add_argument('--min_gain', type=float, default=-1.0)
  parser.add_argument('--max_gain', type=float, default=2.0)
  parser.add_argument('--output_file', required=True)
  args = parser.parse_args()
  utils.configLogging()
  getFeatureGain(args.feature_dir, args.gain_dir, args.ticker_file,
                 args.min_date, args.max_date, args.window,
                 args.min_feature_perc, args.max_feature_perc,
                 args.min_gain, args.max_gain, args.output_file)

if __name__ == '__main__':
  main()

