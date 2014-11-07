import csv
import argparse
parser = argparse.ArgumentParser(description='Scoring for IQ measures.')
parser.add_argument('name', type=str, help='task name')
parser.add_argument('key', type=str, help='file name for task key.  Key should be a csv with 1 row.  First cell is ignored')
parser.add_argument('data', type=str, help='data file with hdr.  subjects on rows, items on columns')
parser.add_argument('out', type=str, help='output file name (outputs as CSV)')
parser.add_argument('out_ttl', type=str, help='output file name for single score per participant')
args = parser.parse_args()

writer = csv.writer(open(args.out,'w'))
writer_ttl = csv.writer(open(args.out_ttl, 'w'))

data = csv.reader(open(args.data, 'r'))
key = csv.reader(open(args.key, 'r')).next()

def compare(key, resp):
    """Compare is resp equals key OR that they're equal when one is reversed (for CFT)"""
    if key == resp or key == reversed(resp): return 1
    else: return 0

hdr = data.next()
L = [ [sub[0]] + map(compare, sub[1:], key[1:]) for sub in data]
Ttl = [ [row[0], sum(row[1:])] for row in L]

writer.writerow(hdr)
writer.writerows(L)
writer_ttl.writerow(['Subject', 'IQ_'+args.name])
writer_ttl.writerows(Ttl)
