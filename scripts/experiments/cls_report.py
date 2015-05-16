#!/usr/bin/python

from sklearn.metrics import classification_report
import exp_utils
import numpy
import pickle

exp_dir = '/Users/lnyang/lab/qd/data/experiments/N'
model_dir = '%s/models' % exp_dir
train_dir = '%s/train' % exp_dir
validate_dir = '%s/validate' % exp_dir
test_dir = '%s/test' % exp_dir

models = exp_utils.getModels(model_dir)
print 'reports for %d models: %s' % (len(models), models)

for model_file in models:
  with open('%s/%s' % (model_dir, model_file), 'rb') as fp:
    model = pickle.load(fp)
  print 'model: %s' % model_file
  for data_dir in [train_dir, validate_dir, test_dir]:
    print 'dir: %s' % data_dir
    data = numpy.loadtxt('%s/data' % data_dir)
    label = numpy.loadtxt('%s/label' % data_dir)
    pred = model.predict(data)
    print classification_report(label, pred)

