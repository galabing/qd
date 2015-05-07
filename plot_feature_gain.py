#!/usr/bin/python

from matplotlib import pyplot
import argparse
import random

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_file', required=True,
                      help='the feature_gain file to plot')
  parser.add_argument('--sample_size', type=int, default=10000)
  parser.add_argument('--minx', type=float, default=float('-Inf'))
  parser.add_argument('--maxx', type=float, default=float('Inf'))
  parser.add_argument('--miny', type=float, default=float('-Inf'))
  parser.add_argument('--maxy', type=float, default=float('Inf'))
  args = parser.parse_args()

  with open(args.input_file, 'r') as fp:
    lines = fp.read().splitlines()
  if len(lines) > args.sample_size:
    lines = random.sample(lines, args.sample_size)
  x = []
  y = []
  skip_stats = {'minx': 0, 'maxx': 0, 'miny': 0, 'maxy': 0}
  for line in lines:
    ticker, feature_date, feature, gain_date, gain = line.split('\t')
    feature = float(feature)
    gain = float(gain)
    if feature < args.minx:
      skip_stats['minx'] += 1
      continue
    if feature > args.maxx:
      skip_stats['maxx'] += 1
      continue
    if gain < args.miny:
      skip_stats['miny'] += 1
      continue
    if gain > args.maxy:
      skip_stats['maxy'] += 1
      continue
    x.append(feature)
    y.append(gain)
  print 'skip_stats: %s' % skip_stats
  pyplot.scatter(x, y, marker='.', s=5, linewidth=0)
  pyplot.axhline(y=sum(y)/len(y), color='r')
  pyplot.show()

if __name__ == '__main__':
  main()

