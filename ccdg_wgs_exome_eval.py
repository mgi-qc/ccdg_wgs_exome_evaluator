import sys
import csv
import os

"""
ccdg_wgs_exome_eval.py

Determine 1x sample status, Fail, WGS topup or Exome.

Usage:

python3 ccdg_wgs_exome_eval.py <infile>

Results outfile: 
wgs_exome_results.tsv
"""

infile = sys.argv[1]
if not os.path.isfile(infile):
    sys.exit('{} file not found.'.format(infile))

with open(infile, 'r') as f, open('wgs_exome_results.tsv', 'w') as o:

    fh = csv.DictReader(f, delimiter='\t')
    o_writer = csv.DictWriter(o, fieldnames=fh.fieldnames + ['WGS_Exome'], delimiter='\t')
    o_writer.writeheader()

    for line in fh:
        last_line = fh.line_num

        line['WGS_Exome'] = 'Fail'
        if 'FREEMIX' not in line['QC Failed Metrics']:
            if float(line['HAPLOID_COVERAGE']) >= 0.85 and float(line['ALIGNMENT_RATE']) >= 0.85:
                line['WGS_Exome'] = 'WGS_Topup'
            else:
                line['WGS_Exome'] = 'Exome'

        o_writer.writerow(line)



