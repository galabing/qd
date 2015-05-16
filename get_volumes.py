#!/usr/bin/python

""" Collects (adj) volume data.

    Example usage:
      ./get_volumes.py --eod_dir=./eod/raw
                       --ticker_file=./tickers
                       --volume_dir=./eod/volumes
                       --use_raw
    or
      ./get_volumes.py --eod_dir=./eod/raw
                       --ticker_file=./tickers
                       --volume_dir=./eod/volumes
                       --take_log

    Average (adj) volume for each month is collected for each ticker.

    Test: spot checked the last month for AAPL, comparing with raw data.
"""

import argparse
import logging
import math
import utils

def getVolume(volumes, take_log):
  volume = sum(volumes)/len(volumes)
  if not take_log: return volume
  if volume <= 0: return None
  return math.log(volume)

def getVolumes(eod_dir, ticker_file, use_raw, take_log, volume_dir):
  tickers = utils.readTickers(ticker_file)
  logging.info('processing %d tickers' % len(tickers))

  for ticker in tickers:
    with open('%s/%s' % (eod_dir, ticker), 'r') as fp:
      lines = fp.read().splitlines()
    prev_date = None
    volumes = []
    count = 0
    with open('%s/%s' % (volume_dir, ticker), 'w') as fp:
      for line in lines:
        items = line.split(',')
        assert len(items) == 14
        date = items[1]
        if use_raw:
          volume = items[6]
        else:
          volume = items[-1]
        if date == '' or volume == '':
          continue
        date = utils.getYm(date)
        volume = float(volume)
        if date == prev_date:
          volumes.append(volume)
          continue
        if prev_date is not None:
          output = getVolume(volumes, take_log)
          if output is not None:
            print >> fp, '%s-01\t%f' % (prev_date, output)
            count += 1
        prev_date = date
        volumes = [volume]
      if prev_date is not None:
        output = getVolume(volumes, take_log)
        if output is not None:
          print >> fp, '%s-01\t%f' % (prev_date, output)
          count += 1
    logging.info('%s: %d volumes' % (ticker, count))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--eod_dir', required=True)
  parser.add_argument('--ticker_file', required=True)
  parser.add_argument('--volume_dir', required=True)
  parser.add_argument('--use_raw', action='store_true',
                      help='use raw instead of adj volume')
  parser.add_argument('--take_log', action='store_true',
                      help='take log of volume')
  args = parser.parse_args()
  utils.configLogging()
  getVolumes(args.eod_dir, args.ticker_file, args.use_raw, args.take_log,
             args.volume_dir)

if __name__ == '__main__':
  main()

