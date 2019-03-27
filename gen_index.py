#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import json
import multiprocessing as mp


def worker_aminer_v2(opath, ipath, index_es):
    """Worker handling Aminer V2 data.

    Parameters
    ----------
    opath : str
        Output directory.
    ipath : str
        Input file.
    index_es : str
        Index name.

    """

    opath = os.path.join(opath, os.path.basename(ipath) + '.index')
    with open(ipath, 'r') as ifp, open(opath, 'w') as ofp:
        for paper in ifp:
            paper = json.loads(paper)
            if 'id' not in paper or 'year' not in paper:
                continue
            index = {'index': {'_index': index_es}}
            pid, year = paper['id'], paper['year']
            venue = paper.get('venue', {})
            paper = {'year': year,
                     'title': paper['title'].lower().strip(),
                     'abstract': paper['abstract'].lower(),
                     'keywords': [e.lower().strip()
                                  for e in paper.get('keywords', [])],
                     'id': pid}
            if 'id' in venue and venue['id']:
                paper['venue_id'] = venue['id']
            if 'raw' in venue and venue['raw']:
                paper['venue_raw '] = venue['raw'].lower().strip()
            json.dump(index, ofp)
            ofp.write('\n')
            json.dump(paper, ofp)
            ofp.write('\n')


def worker_mag_v1(opath, ipath, index_es):
    """Worker handling MAG V1 data.

    Parameters
    ----------
    opath : str
        Output directory.
    ipath : str
        Input file.
    index_es : str
        Index name.

    """

    opath = os.path.join(opath, os.path.basename(ipath) + '.index')
    with open(ipath, 'r') as ifp, open(opath, 'w') as ofp:
        for paper in ifp:
            paper = json.loads(paper)
            if 'id' not in paper or 'year' not in paper:
                continue
            pid, year = paper['id'], paper['year']
            index = {'index': {'_index': index_es}}
            paper = {'year': year,
                     'title': paper['title'].lower().strip(),
                     'abstract': paper['abstract'].lower(),
                     'fos': [e.lower().strip() for e in paper.get('fos', [])],
                     'keywords': [e.lower().strip()
                                  for e in paper.get('keywords', [])],
                     'venue': paper.get('venue', '').lower().strip(),
                     'id': pid}
            json.dump(index, ofp)
            ofp.write('\n')
            json.dump(paper, ofp)
            ofp.write('\n')


if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    group = pparser.add_mutually_exclusive_group(required=True)
    group.add_argument('--aminer_v2', action='store_true',
                       help='use Aminer v2')
    group.add_argument('--mag_v1', action='store_true', help='use MAG v1')
    pparser.add_argument('--index', type=str, default='mag_v1',
                         help='index name used in elasticsearch')
    pparser.add_argument('--cores', type=int, default=2,
                         help='Number of cores to use')
    pparser.add_argument('--output', required=True, help='output path')
    pparser.add_argument('--inputs', required=True, nargs='+',
                         help='input paths')
    args = pparser.parse_args()
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    pool = mp.Pool(args.cores)
    for ipath in args.inputs:
        if args.aminer_v2:
            res = pool.apply_async(worker_aminer_v2, args=(args.output, ipath,
                                                           args.index, ))
        elif args.mag_v1:
            res = pool.apply_async(worker_mag_v1, args=(args.output, ipath,
                                                        args.index, ))
    print(res.get())
    pool.close()
    pool.join()
