import logging

def configLogging(level=logging.INFO):
  logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s',
                      level=level)

def getY(ymd):
  y, m, d = ymd.split('-')
  return y

def getYm(ymd):
  y, m, d = ymd.split('-')
  return '%s-%s' % (y, m)

def getNextYm(ym, k=1):
  assert k >= 0
  y, m = ym.split('-')
  y = int(y)
  m = int(m)
  y += int(k/12)
  m += k % 12
  if m > 12:
    m -= 12
    y += 1
  return '%02d-%02d' % (y, m)

def updateCountDict(count_dict, key):
  if key not in count_dict: count_dict[key] = 1
  else: count_dict[key] += 1

def updateListDict(list_dict, key, value):
  if key not in list_dict: list_dict[key] = [value]
  else: list_dict[key].append(value)

def readL1(lines):
  """ Reads l1 file into a dict: date => {indicator: value}.
  """
  assert len(lines) > 0
  headers = lines[0].split('\t')
  assert len(headers) > 0
  assert all([header != '' for header in headers])
  assert headers[0] == 'date'
  data = dict()
  for i in range(1, len(lines)):
    items = lines[i].split('\t')
    assert len(items) == len(headers)
    row = dict()
    for j in range(1, len(headers)):
      if items[j] != '':
        row[headers[j]] = float(items[j])
    data[items[0]] = row
  return data

def computeFeatureStats(features):
  """ Computes feature stats.
      features: [(y, f), (y, f), ...] where f is either float or None
                indicating nonexistent feature value.
      returns: dict of y => [count, total, avg, min, 1p, 10p, 25p, 50p,
                             75p, 90p, 99p, max]
      Feature coverage = count / total, eg.
  """
  ncounts = dict()  # y => #None
  values = dict()  # y => [non-None values]
  for y, f in features:
    if f is None:
      updateCountDict(ncounts, y)
    else:
      updateListDict(values, y, f)
  stats = dict()
  for y, v in values.iteritems():
    v.sort()
    lenv = len(v)
    stats[y] = [lenv, lenv + ncounts.get(y, 0), sum(v)/lenv, v[0],
                v[int(lenv*0.01)], v[int(lenv*0.1)],
                v[int(lenv*0.25)], v[int(lenv*0.5)],
                v[int(lenv*0.75)], v[int(lenv*0.9)],
                v[int(lenv*0.99)], v[-1]]
  for y, n in ncounts.iteritems():
    if y not in stats:
      stats[y] = [0, n, None, None, None, None, None, None, None,
                  None, None, None]
  return stats

