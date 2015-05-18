#!/usr/bin/python

""" Collects log(x) for yahoo data.

    Example usage:
      ./get_yahoo_log_data.py --input_file=./prices/SP500
                              --output_file=./logprices/SP500
"""

import argparse
import math

def getLogData(input_file, output_file):
  with open(input_file, 'r') as fp:
    lines = fp.read().splitlines()
  with open(output_file, 'w') as fp:
    for line in lines:
      date, value = line.split('\t')
      value = float(value)
      if value > 0:
        print >> fp, '%s\t%f' % (date, math.log(value))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_file', required=True)
  parser.add_argument('--output_file', required=True)
  args = parser.parse_args()
  getLogData(args.input_file, args.output_file)

if __name__ == '__main__':
  main()

