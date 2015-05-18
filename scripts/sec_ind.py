#!/usr/bin/python

""" Confusion matrix between sector and industry.
"""

input_file = '/Users/lnyang/lab/qd/data/sf1_ticker_info.txt'
output_file = '/Users/lnyang/lab/qd/data/misc/sec_ind.tsv'

with open(input_file, 'r') as fp:
  lines = fp.read().splitlines()
assert len(lines) > 0
headers = lines[0].split('\t')
assert headers[5] == 'Sector'
assert headers[6] == 'Industry'

sectors = []
industries = []
for i in range(1, len(lines)):
  items = lines[i].split('\t')
  sectors.append(items[5])
  industries.append(items[6])

sector_headers = sorted(set(sectors))
industry_headers = sorted(set(industries))
print 'sectors:'
for sector in sector_headers:
  print '  %s' % sector
print 'industries:'
for industry in industry_headers:
  print '  %s' % industry

sector_index = {sector_headers[i]: i+1
                for i in range(len(sector_headers))}
industry_index = {industry_headers[i]: i+1
                  for i in range(len(industry_headers))}

data = [[0 for i in range(len(industry_headers) + 1)]
        for j in range(len(sector_headers) + 1)]
data[0][0] = 'Sector\\Industry'
for i in range(len(sector_headers)):
  data[i+1][0] = sector_headers[i]
for i in range(len(industry_headers)):
  data[0][i+1] = industry_headers[i]
for i in range(len(sectors)):
  sec = sector_index[sectors[i]]
  ind = industry_index[industries[i]]
  data[sec][ind] += 1

with open(output_file, 'w') as fp:
  for row in data:
    print >> fp, '\t'.join([str(item) for item in row])

