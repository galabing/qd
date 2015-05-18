#!/usr/bin/python

from sklearn import tree
from sklearn.externals.six import StringIO
import pickle
import pydot

model_file = '/Users/lnyang/lab/qd/data/experiments/M/models/RandomForestClassifier-10-2'
vis_dir = '/Users/lnyang/lab/qd/data/experiments/M/vismodels/RandomForestClassifier-10-2'

with open(model_file, 'rb') as fp:
  model = pickle.load(fp)

for i in range(len(model.estimators_)):
  print 'visualizing tree %d/%d' % (i+1, len(model.estimators_))
  dot_data = StringIO()
  tree.export_graphviz(model.estimators_[i], out_file=dot_data)
  graph = pydot.graph_from_dot_data(dot_data.getvalue())
  graph.write_pdf('%s/tree-%d.pdf' % (vis_dir, i))

