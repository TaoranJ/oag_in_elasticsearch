# -*- coding: utf-8 -*-

import os
import json
import argparse
from collections import defaultdict

import elasticsearch
import elasticsearch.helpers


def query_fos(args):
    if not os.path.exists(args.opath):
        os.makedirs(args.opath)
    with open(args.seed, 'r') as ifp:
        for seed in ifp:
            seed = seed.strip()
            query = {'query': {'match_phrase': {'fos.keyword': seed}}}
            es = elasticsearch.Elasticsearch()
            res = elasticsearch.helpers.scan(es, index='publication',
                                             preserve_order=True, query=query)
            pids = defaultdict(list)
            for data in res:
                pids[data['_source']['year']].append(data['_id'])
            for year, ids in pids.items():
                json.dump(ids, open(os.path.join(
                    args.opath, str(year) + '.' + str(seed) + '.json'), 'w'))


if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    pparser.add_argument('seed', help='path to seed query')
    pparser.add_argument('opath', help='output directory')
    args = pparser.parse_args()
    query_fos(args)
