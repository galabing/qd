#!/usr/bin/python

from sklearn import tree
from sklearn.externals.six import StringIO
import os
import pickle
import pydot

model_file = '/Users/lnyang/lab/qd/data/experiments/S/models/RandomForestClassifier-100-2-201305--1'
vis_dir = '/Users/lnyang/lab/qd/data/experiments/S/vismodels/RandomForestClassifier-100-2-201305--1'

with open(model_file, 'rb') as fp:
  model = pickle.load(fp)

if not os.path.isdir(vis_dir):
  os.mkdir(vis_dir)

for i in range(len(model.estimators_)):
  print 'visualizing tree %d/%d' % (i+1, len(model.estimators_))
  dot_data = StringIO()
  tree.export_graphviz(model.estimators_[i], out_file=dot_data)
  graph = pydot.graph_from_dot_data(dot_data.getvalue())
  graph.write_pdf('%s/tree-%d.pdf' % (vis_dir, i))

