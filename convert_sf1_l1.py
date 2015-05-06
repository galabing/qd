#!/usr/bin/python

""" Converts raw files into level-1 features.

    Usage:
      ./convert_sf1_l1.py --raw_dir=./raw
                          --l1_dir=./l1

    For each ticker file in raw_dir, one or more files will be created in
    l1_dir/<ticker>, one for each dimension.  Output files are in tsv format,
    with first column being date, and the rest being sorted indicators.
    Rows are sorted by date.

    The current output format is a compromise between readability and data
    size.  Dimensions like ARQ are pretty dense (a ticker tends to have the
    same set of indicators in every ARQ) so size wise this is good.  ND tends
    to be very sparse, but ND itself doesn't have much data.

    Test: https://docs.google.com/spreadsheets/d/1rgq4S3Nijrzt9o8-hrxcPbFErTKcdjJ_e68QpU4UPyo/edit#gid=0
    Manually verified cells B2, B9, P13, AX46 for AAPL-ARQ and B2, G9, J209
    for AAPL-ND by comparing against the raw file.
"""

import argparse
import logging
import os
import utils

OUTPUT_DELIM = '\t'
OUTPUT_SUFFIX = '.tsv'
# Output file name for empty dimension.
NO_DIMENSION = 'ND'
DATE_HEADER = 'date'
NO_VALUE = ''

def readRawDict(raw_file):
  with open(raw_file, 'r') as fp:
    lines = fp.read().splitlines()
  # dimension => { date => { indicator => value } }
  raw_dict = dict()
  for line in lines:
    label, date, value = line.split(',')
    items = label.split('_')
    assert len(items) == 2 or len(items) == 3
    assert items[0] == raw_file[raw_file.rfind('/')+1:]
    indicator = items[1]
    assert indicator != DATE_HEADER
    if len(items) == 2:
      dimension = NO_DIMENSION
    else:
      assert items[2] != NO_DIMENSION
      dimension = items[2]
    if dimension not in raw_dict:
      raw_dict[dimension] = {date: {indicator: value}}
    elif date not in raw_dict[dimension]:
      raw_dict[dimension][date] = {indicator: value}
    else:
      assert indicator not in raw_dict[dimension][date]
      raw_dict[dimension][date][indicator] = value
  return raw_dict

def convertSf1L1(raw_dir, l1_dir, overwrite=False):
  raw_files = sorted(os.listdir(raw_dir))
  logging.info('processing %d raw files' % len(raw_files))
  for i in range(len(raw_files)):
    ticker = raw_files[i]
    logging.info('processing %d/%d: %s' % (i+1, len(raw_files), ticker))
    output_dir = '%s/%s' % (l1_dir, ticker)
    if os.path.isdir(output_dir):
      if not overwrite:
        logging.info('output exists, skipping: %s' % ticker)
        continue
    else:
      os.mkdir(output_dir)
    raw_file = '%s/%s' % (raw_dir, ticker)
    raw_dict = readRawDict(raw_file)
    for dimension, date_dict in raw_dict.iteritems():
      # Get sorted dates for this ticker dimension.
      dates = sorted(date_dict.keys())
      date_index = {dates[i]: i for i in range(len(dates))}
      # Get sorted indicators for this ticker dimension.
      indicators = set()
      for indicator_dict in date_dict.itervalues():
        indicators.update(indicator_dict.iterkeys())
      indicators = sorted(indicators)
      # Index for indicators start from 1 because the first column is date.
      indicator_index = {indicators[i]: i+1 for i in range(len(indicators))}
      # Prepare the header for tsv output.
      header = [DATE_HEADER] + indicators
      # Prepare the matrix for tsv output.
      data = [[NO_VALUE for i in range(len(indicators)+1)]
              for j in range(len(dates))]
      for date, indicator_dict in date_dict.iteritems():
        row = date_index[date]
        # Fill in the first column (date).
        data[row][0] = date
        # Fill in the other columns (indicators).
        for indicator, value in indicator_dict.iteritems():
          data[row][indicator_index[indicator]] = value
      # Write output.
      with open('%s/%s%s' % (output_dir, dimension, OUTPUT_SUFFIX), 'w') as fp:
        print >> fp, OUTPUT_DELIM.join(header)
        for row in data:
          print >> fp, OUTPUT_DELIM.join(row)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--raw_dir', required=True,
                      help='input dir of raw data files')
  parser.add_argument('--l1_dir', required=True,
                      help='output dir of level-1 feature files')
  parser.add_argument('--overwrite', action='store_true',
                      help='overwrite existing files in output dir')
  args = parser.parse_args()
  utils.configLogging()
  convertSf1L1(args.raw_dir, args.l1_dir, args.overwrite)

if __name__ == '__main__':
  main()

