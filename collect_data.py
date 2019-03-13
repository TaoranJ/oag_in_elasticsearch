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
    queries = json.load(open(args.seed, 'r'))
    pids = set()
    opath = os.path.join(args.opath, os.path.basename(args.seed))
    with open(opath, 'w') as ofp:
        for ix, query in enumerate(queries, start=1):
            print('[BATCH {:03d}/{:03d}]'.format(ix, len(queries)))
            query = {'query': {'match_phrase': {'fos.keyword': query.strip()}}}
            es = elasticsearch.Elasticsearch()
            res = elasticsearch.helpers.scan(es, index='mag_v1', query=query,
                                             request_timeout=50)
            for data in res:
                pid =  data['_id']
                if pid not in pids:
                    pids.add(pid)
                    json.dump({'id': pid, **data['_source']}, ofp)
                    ofp.write('\n')


if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    pparser.add_argument('seed', help='path to seed query')
    pparser.add_argument('opath', help='output directory')
    args = pparser.parse_args()
    query_fos(args)
