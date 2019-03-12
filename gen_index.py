#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import json
import multiprocessing as mp

def worker(opath, ipath, index_es):
    opath = os.path.join(opath, os.path.basename(ipath) + '.index')
    with open(ipath, 'r') as ifp, open(opath, 'w') as ofp:
        for paper in ifp:
            paper = json.loads(paper)
            if 'id' not in paper or 'year' not in paper:
                continue
            pid, year = paper['id'], paper['year']
            index = {'index': {'_index': index_es, '_id': pid}}
            paper = {'year': year,
                     'title': paper['title'].lower().strip(),
                     'abstract': paper['abstract'].lower(),
                     'fos': [e.lower().strip() for e in paper.get('fos', [])],
                     'keywords': [e.lower().strip()
                                  for e in paper.get('keywords', [])]}
            json.dump(index, ofp)
            ofp.write('\n')
            json.dump(paper, ofp)
            ofp.write('\n')

if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    pparser.add_argument('--index', type=str, default='mag_v1',
                         help='index name used in elasticsearch')
    pparser.add_argument('--cores', type=int, default=2,
                         help='Number of cores to use')
    pparser.add_argument('--output', required=True, help='output path')
    pparser.add_argument('--input', required=True, nargs='+',
                         help='input paths')
    args = pparser.parse_args()
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    pool = mp.Pool(args.cores)
    for ipath in args.input:
        res = pool.apply_async(worker, args=(args.output, ipath, args.index, ))
    print(res.get())
    pool.close()
    pool.join()
