#!/usr/bin/python

import exp_utils

exp_dir = '/Users/lnyang/lab/qd/data/experiments/I'
model_dir = '%s/models' % exp_dir
validate_dir = '%s/validate' % exp_dir
num_buckets = 50
distr_file = '%s/distr-%d.tsv' % (validate_dir, num_buckets)

models = exp_utils.getModels(model_dir)
print 'validating %d models: %s' % (len(models), models)

distr_fp = open(distr_file, 'w')
print >> distr_fp, 'model\t%s\tavg' % ('\t'.join([
    str(i) for i in range(1, num_buckets+1)]))

for model in models:
  model_file = '%s/%s' % (model_dir, model)
  data_file = '%s/data' % validate_dir
  label_file = '%s/label' % validate_dir
  meta_file = '%s/meta' % validate_dir
  distr = exp_utils.computeGainDistribution(
      model_file, data_file, label_file, meta_file, num_buckets)
  avg = sum(distr)/len(distr)
  print >> distr_fp, '%s\t%s\t%f' % (
      model, '\t'.join(['%f' % d for d in distr]), avg)
distr_fp.close()

