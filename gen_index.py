#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import json
import multiprocessing as mp

def worker(opath, ipath):
    opath = os.path.join(opath, os.path.basename(ipath) + '.index')
    with open(ipath, 'r') as ifp, open(opath, 'w') as ofp:
        for paper in ifp:
            paper = json.loads(paper)
            if 'id' not in paper or 'year' not in paper:
                continue
            pid, year = paper['id'], paper['year']
            index = {'index': {'_index': 'publication', '_id': pid}}
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
    pparser.add_argument('opath', help='output path')
    pparser.add_argument('ipaths', nargs='+', help='input paths')
    args = pparser.parse_args()
    if not os.path.exists(args.opath):
        os.makedirs(args.opath)
    pool = mp.Pool(4)
    for ipath in args.ipaths:
        res = pool.apply_async(worker, args=(args.opath, ipath,))
    print(res.get())
    pool.close()
    pool.join()
