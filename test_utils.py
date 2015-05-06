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

