#!/usr/bin/python

import exp_utils

exp_dir = '/Users/lnyang/lab/qd/data/experiments/C'
model_dir = '%s/models' % exp_dir
validate_dir = '%s/validate' % exp_dir
data_file = '%s/data' % validate_dir
label_file = '%s/label' % validate_dir
meta_file = '%s/meta' % validate_dir

model = 'Ridge-1.000000-1.000000'
num_buckets = 50
distr_file = '%s/distr-detail-%d.tsv' % (validate_dir, num_buckets)

print 'validating %s with %d buckets' % (model, num_buckets)

distr_fp = open(distr_file, 'w')
print >> distr_fp, 'date\t%s\tavg' % ('\t'.join([
    str(i) for i in range(1, num_buckets+1)]))

model_file = '%s/%s' % (model_dir, model)
distrs = exp_utils.computeDetailedGainDistribution(
    model_file, data_file, label_file, meta_file, num_buckets)
for ym in sorted(distrs.keys()):
  distr = distrs[ym]
  avg = sum(distr)/len(distr)
  print >> distr_fp, '%s\t%s\t%f' % (
      ym, '\t'.join(['%f' % d for d in distr]), avg)
distr_fp.close()

