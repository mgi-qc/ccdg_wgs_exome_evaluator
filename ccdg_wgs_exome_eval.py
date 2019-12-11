import sys
import csv
import os

"""
ccdg_wgs_exome_eval.py

Determine 1x sample status, Fail, WGS topup or Exome.

infile format: 2859333.85.120219.build38.all.tsv
Usage:

python3 ccdg_wgs_exome_eval.py <infile> 
python3 ccdg_wgs_exome_eval.py <infile>,<infile2>,<infile3>...

Results outfile: 
2859333.85.120219.wgs_exome_results.tsv
"""

for infile in sys.argv[1].split(','):

    if not os.path.isfile(infile):
        sys.exit('{} file not found.'.format(infile))

    assert len(infile.split('.')[:3]) == 3, '<infile> format not correct.'

    outfile = '{}.wgs_exome_results.tsv'.format('.'.join(infile.split('.')[:3]))

    with open(infile, 'r') as f, open(outfile, 'w') as o:

        fh = csv.DictReader(f, delimiter='\t')
        o_writer = csv.DictWriter(o, fieldnames=fh.fieldnames + ['WGS_Exome'], delimiter='\t')
        o_writer.writeheader()

        for line in fh:

            line['WGS_Exome'] = 'Fail'
            if 'FREEMIX' not in line['QC Failed Metrics']:
                if 'HAPLOID_COVERAGE' in line['QC Failed Metrics'] and float(line['ALIGNMENT_RATE']) >= 0.85:
                    line['WGS_Exome'] = 'WGS_Topup'
                else:
                    line['WGS_Exome'] = 'Exome'

            o_writer.writerow(line)



