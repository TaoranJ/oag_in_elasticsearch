# -*- coding: utf-8 -*-

import argparse

from mag import MAG

if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    pparser.add_argument('--input', required=True, help='input file')
    pparser.add_argument('--output', required=True, help='output directory')
    pparser.add_argument('--index', type=str, default='mag_v1',
                         help='index of mag in elasticsearch')
    args = pparser.parse_args()
    inst = MAG(query_file=None, output_dir=args.output, index=args.index,
               min_year=None, max_year=None)
    inst.keyword_gen(args.input)
