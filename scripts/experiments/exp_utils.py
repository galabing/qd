import numpy
import os
import pickle
import sys

def run(cmd):
  print 'running command: %s' % cmd
  sys.stdout.flush()
  assert os.system(cmd) == 0

def trainModel(trainer, data_file, label_file, model_def, perc, model_file):
  cmd = ('%s --data_file=%s --label_file=%s --model_def=\'%s\' --perc=%f '
         '--model_file=%s' % (trainer, data_file, label_file, model_def,
                              perc, model_file))
  run(cmd)

def computeError(model_file, data_file, label_file):
  print 'computing error for'
  print '  model: %s' % model_file
  print '  data: %s' % data_file
  print '  label: %s' % label_file
  with open(model_file, 'rb') as fp:
    model = pickle.load(fp)
  print 'model: %s' % model
  X = numpy.loadtxt(data_file)
  print 'X.shape: %s' % str(X.shape)
  y = numpy.loadtxt(label_file)
  print 'y.shape: %s' % str(y.shape)

  p = model.predict(X)
  m = X.shape[0]
  se = ((y - p) ** 2).sum()
  r2 = model.score(X, y)
  return m, se, r2

