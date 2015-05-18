#!/usr/bin/python

""" Collects monthly average volumes for yahoo data.

    Example usage:
      ./get_yahoo_volumes.py --input_file=./yahoo_sp500.csv
                             --output_file=./SP500

    Average volume for each month is collected.
    Tested by spot checking a few entries for SP500.
"""

import argparse
import datetime
import logging
import utils

def getVolumes(input_file, output_file):
  with open(input_file, 'r') as fp:
    lines = fp.read().splitlines()
  assert len(lines) > 0
  assert lines[0] == 'Date,Open,High,Low,Close,Volume,Adj Close'
  lines = lines[1:]
  lines.reverse()  # Yahoo dates are sorted desc.
  prev_ym = None
  volumes = []
  with open(output_file, 'w') as fp:
    for line in lines:
      date, open_, high, low, close, volume, adj_close = line.split(',')
      if date == '':
        logging.warning('empty date in line: %s' % line)
        continue
      if volume == '':
        logging.warning('empty volume in line: %s' % line)
        continue
      try:
        tmp = datetime.datetime.strptime(date, '%Y-%m-%d')
      except ValueError:
        logging.warning('invalid date: %s in line: %s' % (date, line))
        continue
      try:
        volume_f = float(volume)
      except ValueError:
        logging.warning('invlaid volume: %s in line: %s' % (volume, line))
        continue
      ym = utils.getYm(date)
      if ym == prev_ym:
        volumes.append(volume_f)
        continue
      if prev_ym is not None:
        assert ym > prev_ym
        assert len(volumes) < 32
        print >> fp, '%s-01\t%f' % (prev_ym, sum(volumes)/len(volumes))
      prev_ym = ym
      volumes = [volume_f]
    if prev_ym is not None:
      assert len(volumes) < 32
      print >> fp, '%s-01\t%f' % (prev_ym, sum(volumes)/len(volumes))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_file', required=True)
  parser.add_argument('--output_file', required=True)
  args = parser.parse_args()
  utils.configLogging()
  getVolumes(args.input_file, args.output_file)

if __name__ == '__main__':
  main()

