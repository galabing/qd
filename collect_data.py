#!/usr/bin/python

""" Collects data for experiments.

    Example usage:
      ./collect_data.py --gain_dir=./gains/1
                        --feature_base_dir=./features
                        --feature_list=./feature_list
                        --min_date=2005-01-01
                        --max_date=2006-12-31
                        --window=120
                        --min_feature_perc=0.8
                        --data_file=./data
                        --meta_file=./meta

    For each ticker, gains within specified min/max date are collected.
    For each dated gain, features are joined by looking back a specified max
    window and using the most recent value (or 0 if not found).

    Two files are written:
    data_file: matrix of gain + features delimited by tab, features delimited
               by space.  Features are in the same order as specified by
               feature_list.
    meta_file: ticker, gain date and feature count corresponding to each row
               in data_file.
"""

import argparse
import bisect
import datetime
import logging
import os
import utils

DEBUG = False

def readFeatureList(feature_list_file):
  with open(feature_list_file, 'r') as fp:
    return [line for line in fp.read().splitlines()
            if not line.startswith('#')]

def collectData(ticker_file, gain_dir, feature_base_dir, feature_list_file,
                min_date, max_date, window, min_feature_perc,
                data_file, meta_file):
  tickers = utils.readTickers(ticker_file)
  logging.info('processing %d tickers' % len(tickers))

  feature_list = readFeatureList(feature_list_file)
  logging.info('using %d features' % len(feature_list))
  for feature in feature_list:
    logging.info('  %s' % feature)
  min_feature_count = int(len(feature_list) * min_feature_perc)

  data_fp = open(data_file, 'w')
  meta_fp = open(meta_file, 'w')

  skip_stats = {'gain_file': 0,
                'feature_file': 0,
                'index': 0,
                'min_date': 0,
                'max_date': 0,
                'window': 0,
                'min_perc': 0}

  for ticker in tickers:
    logging.info(ticker)

    gain_file = '%s/%s' % (gain_dir, ticker)
    if not os.path.isfile(gain_file):
      logging.info('missing gain file: %s' % gain_file)
      skip_stats['gain_file'] += 1
      continue
    gains = utils.readKeyValueFile(gain_file)

    feature_items = [[] for i in range(len(feature_list))]
    for i in range(len(feature_list)):
      feature_file = '%s/%s/%s' % (feature_base_dir, feature_list[i], ticker)
      if not os.path.isfile(feature_file):
        skip_stats['feature_file'] += 1
        continue
      feature_items[i] = utils.readKeyValueFile(feature_file)

    for gain_date, gain in gains:
      if gain_date < min_date:
        skip_stats['min_date'] += 1
        continue
      if gain_date > max_date:
        skip_stats['max_date'] += 1
        continue

      if DEBUG:
        print 'gain: %f (%s)' % (gain, gain_date)

      features = [0.0 for i in range(len(feature_list))]
      feature_count = 0
      for i in range(len(feature_list)):
        feature_dates = [item[0] for item in feature_items[i]]
        index = bisect.bisect_right(feature_dates, gain_date) - 1
        if index < 0:
          skip_stats['index'] += 1
          continue

        gain_date_obj = datetime.datetime.strptime(gain_date, '%Y-%m-%d')
        feature_date_obj = datetime.datetime.strptime(feature_dates[index],
                                                      '%Y-%m-%d')
        delta = (gain_date_obj - feature_date_obj).days
        if delta > window:
          skip_stats['window'] += 1
          continue

        if DEBUG:
          print 'feature %s: (%s, %f)' % (
              feature_list[i], feature_items[i][index][0],
              feature_items[i][index][1])

        features[i] = feature_items[i][index][1]
        feature_count += 1

      if feature_count < min_feature_count:
        skip_stats['min_perc'] += 1
        continue

      print >> data_fp, '%f\t%s' % (gain, ' '.join(
          ['%f' % feature for feature in features]))
      print >> meta_fp, '%s\t%s\t%d' % (ticker, gain_date, feature_count)

    if DEBUG: break

  data_fp.close()
  meta_fp.close()
  logging.info('skip_stats: %s' % skip_stats)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--gain_dir', required=True)
  parser.add_argument('--feature_base_dir', required=True)
  parser.add_argument('--feature_list', required=True)
  parser.add_argument('--min_date', default='0000-00-00')
  parser.add_argument('--max_date', default='9999-99-99')
  # Most features have a max lag of one quarter.
  parser.add_argument('--window', type=int, default=120)
  parser.add_argument('--min_feature_perc', type=float, default=0.8,
                      help='only use a feature vector if at least certain '
                           'perc of features are populated')
  parser.add_argument('--data_file', required=True)
  parser.add_argument('--meta_file', required=True)
  args = parser.parse_args()
  utils.configLogging()
  collectData(args.ticker_file, args.gain_dir, args.feature_base_dir,
              args.feature_list, args.min_date, args.max_date, args.window,
              args.min_feature_perc, args.data_file, args.meta_file)

if __name__ == '__main__':
  main()

