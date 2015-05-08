#!/usr/bin/python

""" Collects adj close for yahoo data.

    Example usage:
      ./get_yahoo_prices.py --input_file=./yahoo_sp500.csv
                            --output_file=./SP500

    Valid adj close from first trading day of each month is collected.
    Tested by spot checking a few entries for SP500.
"""

import argparse
import datetime
import logging
import utils

def getPrices(input_file, output_file):
  with open(input_file, 'r') as fp:
    lines = fp.read().splitlines()
  assert len(lines) > 0
  assert lines[0] == 'Date,Open,High,Low,Close,Volume,Adj Close'
  lines = lines[1:]
  lines.reverse()  # Yahoo dates are sorted desc.
  prev_ym = None
  with open(output_file, 'w') as fp:
    for line in lines:
      date, open_, high, low, close, volume, adj_close = line.split(',')
      if date == '':
        logging.warning('empty date in line: %s' % line)
        continue
      if adj_close == '':
        logging.warning('empty adj close in line: %s' % line)
        continue
      try:
        tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
      except ValueError:
        logging.warning('invalid date: %s in line: %s' % (date, line))
        continue
      try:
        adj_close_f = float(adj_close)
      except ValueError:
        logging.warning('invlaid adj close: %s in line: %s' % (adj_close, line))
        continue
      if adj_close_f < 0:
        logging.warning('invalid adj close: %s in line: %s' % (adj_close, line))
        continue
      ym = utils.getYm(date)
      if ym == prev_ym:
        continue
      assert ym > prev_ym
      prev_ym = ym
      print >> fp, '%s\t%s' % (date, adj_close)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_file', required=True)
  parser.add_argument('--output_file', required=True)
  args = parser.parse_args()
  utils.configLogging()
  getPrices(args.input_file, args.output_file)

if __name__ == '__main__':
  main()

