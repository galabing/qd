#!/usr/bin/python

""" Collects tickers from SF1 and EOD datasets.

    Example usage:
      ./get_tickers.py --sf1_dir=./sf1/raw
                       --eod_dir=./eod/raw
                       --ticker_file=./tickers

    Common tickers between SF1 ane EOD that pass these checks are collected:
    - end month in EOD is 2015/05
    - no missing month in EOD
    Both should be pretty small subsets.
"""

import argparse
import logging
import os
import utils

TARGET_DATE = '2015-05'

class Status:
  OK = 0
  END = 1
  MISS = 2

def getDate(ymd):
  y, m, d = ymd.split('-')
  return '%s-%s' % (y, m)

def getNextDate(ym):
  y, m = ym.split('-')
  y = int(y)
  m = int(m)
  if m < 12:
    m += 1
  else:
    y += 1
    m = 1
  return '%02d-%02d' % (y, m)

def checkEod(eod_file):
  with open(eod_file, 'r') as fp:
    lines = fp.read().splitlines()
  dates = set()
  for line in lines:
    items = line.split(',')
    assert len(items) == 14
    date = items[1]
    adj_close = items[-1]
    if date == '' or adj_close == '':
      continue
    dates.add(getDate(date))
  min_date = min(dates)
  max_date = max(dates)
  if max_date != TARGET_DATE:
    if max_date > TARGET_DATE:
      logging.warning('max_date exceeds target: %s vs %s' % (
                      max_date, TARGET_DATE))
    return Status.END
  date = min_date
  while date <= max_date:
    if date not in dates:
      return Status.MISS
    date = getNextDate(date)
  return Status.OK

def getTickers(sf1_dir, eod_dir, ticker_file):
  sf1_tickers = set(os.listdir(sf1_dir))
  eod_tickers = set(os.listdir(eod_dir))
  shared_tickers = sf1_tickers & eod_tickers
  logging.info('ticker count: SF1 = %d, EOD = %d, shared = %d' % (
               len(sf1_tickers), len(eod_tickers), len(shared_tickers)))

  tickers = []
  stats = {Status.OK: 0, Status.END: 0, Status.MISS: 0}
  for ticker in shared_tickers:
    status = checkEod('%s/%s' % (eod_dir, ticker))
    stats[status] += 1
    if status == Status.OK:
      tickers.append(ticker)
    else:
      logging.info('dropping ticker %s due to status %d' % (ticker, status))
    
  logging.info('end early: %d, missing months: %d, ok: %d' % (
               stats[Status.END], stats[Status.MISS], stats[Status.OK]))
  with open(ticker_file, 'w') as fp:
    for ticker in sorted(tickers):
      print >> fp, ticker

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--sf1_dir', required=True)
  parser.add_argument('--eod_dir', required=True)
  parser.add_argument('--ticker_file', required=True)
  args = parser.parse_args()
  utils.configLogging()
  getTickers(args.sf1_dir, args.eod_dir, args.ticker_file)

if __name__ == '__main__':
  main()

