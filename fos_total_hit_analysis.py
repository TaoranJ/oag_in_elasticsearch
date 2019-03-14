# -*- coding: utf-8 -*-

import argparse
from mag import MAG

if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    pparser.add_argument('--query', required=True, help='file of queries')
    pparser.add_argument('--opath', required=True, help='output directory')
    pparser.add_argument('--index', type=str, default='mag_v1',
                         help='index of mag in elasticsearch')
    pparser.add_argument('--min-year', type=int, default=2000,
                         help='Min year to consider.')
    pparser.add_argument('--max-year', type=int, default=2018,
                         help='Max year to consider.')
    args = pparser.parse_args()
    inst = MAG(query_file=args.query, output_dir=args.opath, index=args.index,
               min_year=args.min_year, max_year=args.max_year)
    inst.fos_total_hits_analysis()
