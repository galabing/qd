#!/usr/bin/python

""" Trains a model based on training data, labels and model def.
"""

from sklearn.ensemble import *
from sklearn.linear_model import *
from sklearn.svm import *
import argparse
import logging
import numpy
import pickle
import utils

def trainModel(data_file, label_file, model_def, perc, model_file):
  logging.info('loading data file: %s' % data_file)
  X = numpy.loadtxt(data_file)
  logging.info('X.shape: %s' % str(X.shape))

  logging.info('loading label file: %s' % label_file)
  y = numpy.loadtxt(label_file)
  logging.info('y.shape: %s' % str(y.shape))

  if perc < 1:
    logging.info('sampling %f data for training' % perc)
    m = int(X.shape[0] * perc)
    index = numpy.random.permutation(X.shape[0])[:m]
    X = X[index, :]
    y = y[index]
    logging.info('sampled X.shape: %s' % str(X.shape))
    logging.info('sampled y.shape: %s' % str(y.shape))

  logging.info('creating model: %s' % model_def)
  model = eval(model_def)
  logging.info('model: %s' % model)

  logging.info('fitting model')
  model.fit(X, y)
  logging.info('params: %s' % model.get_params())

  with open(model_file, 'wb') as fp:
    pickle.dump(model, fp)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_file', required=True)
  parser.add_argument('--label_file', required=True)
  parser.add_argument('--model_def', required=True,
                      help='string of model def; eg, "Model(alpha=0.5)"')
  parser.add_argument('--perc', type=float, default=1.0,
                      help='if < 1, will randomly sample specified perc '
                           'of data for training')
  parser.add_argument('--model_file', required=True)
  args = parser.parse_args()
  utils.configLogging()
  trainModel(args.data_file, args.label_file, args.model_def, args.perc,
             args.model_file)

if __name__ == '__main__':
  main()

