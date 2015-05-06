import utils

def test_getYm():
  assert utils.getYm('2015-05-05') == '2015-05'
  assert utils.getYm('1984-02-22') == '1984-02'

def test_getNextYm():
  assert utils.getNextYm('2015-05') == '2015-06'
  assert utils.getNextYm('1984-12') == '1985-01'
  assert utils.getNextYm('1984-02', 0) == '1984-02'
  assert utils.getNextYm('1984-02', 1) == '1984-03'
  assert utils.getNextYm('1984-02', 10) == '1984-12'
  assert utils.getNextYm('1984-02', 11) == '1985-01'
  assert utils.getNextYm('1984-02', 123) == '1994-05'

def test_updateCountDict():
  d = dict()
  utils.updateCountDict(d, 'key1')
  assert d == {'key1': 1}
  utils.updateCountDict(d, 'key1')
  assert d == {'key1': 2}
  utils.updateCountDict(d, 'key2')
  assert d == {'key1': 2, 'key2': 1}

def test_updateListDict():
  d = dict()
  utils.updateListDict(d, 'key1', 1)
  assert d == {'key1': [1]}
  utils.updateListDict(d, 'key1', 2)
  assert d == {'key1': [1, 2]}
  utils.updateListDict(d, 'key2', 3)
  assert d == {'key1': [1, 2], 'key2': [3]}

def test_readL1():
  lines = (
      'date\tABC\tXYZ',
      '1984-02-22\t1\t2',
      '2000-01-01\t\t',
      '2015-05-05\t\t-123')
  data = utils.readL1(lines)
  assert data == {
      '1984-02-22': {'ABC': 1.0, 'XYZ': 2.0},
      '2000-01-01': {},
      '2015-05-05': {'XYZ': -123.0}}

def test_computeFeatureStats():
  features = [('1984', None),
              ('1984', 1),
              ('1984', 3),
              ('1984', 5),
              ('1984', 7),
              ('1984', 9),
              ('1984', None),
              ('1984', 10),
              ('1984', 8),
              ('1984', 6),
              ('1984', 4),
              ('1984', 2),
              ('1984', None),
              ('2015', 100),
              ('2000', None),
              ('2000', None)]
  stats = utils.computeFeatureStats(features)
  assert stats == {
      '1984': [10, 13, 5, 1, 1, 2, 3, 6, 8, 10, 10, 10],
      '2000': [0, 2, None, None, None, None, None, None,
               None, None, None, None],
      '2015': [1, 1, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]}

