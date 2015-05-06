import logging

def configLogging(level=logging.INFO):
  logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s',
                      level=level)

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

