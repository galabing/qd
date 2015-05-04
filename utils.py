import logging

def configLogging(level=logging.INFO):
  logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s',
                      level=level)

