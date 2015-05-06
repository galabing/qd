#!/usr/bin/python

""" Collects some data points for plotting, usually with first column
    being feature values and second column being labels (gains).

    Example usage:
      ./get_xy.py --feature_dir=./ebitev
                  --gain_dir=./gains12
                  --ticker_file=./tickers
                  --min_date=2004-01-01
                  --max_date=2009-12-31
                  --window=60
                  --min_feature_perc=0.01
                  --max_feature_perc=0.99
                  --min_gain=-1
                  --max_gain=1
                  --xy_file=./ebitev-12.tsv
"""

import argparse
import bisect
import logging
import os
import utils

def main():
  pass

if __name__ == '__main__':
  main()

