# -*- coding: utf-8 -*-

import os
import argparse
import json
import time

from tqdm import tqdm

from utils import split_file
from es import create_index_aminer_v1, refresh, bulk_insert
from es import delete_index, update_settings

drop_count = 0


def index_worker(index, ipath):
    """Indexing.

    Parameters
    ----------
    index : str
        Name of index.
    ipath : str
        Path to raw json files.

    """

    opath = os.path.join('tmp.json')
    for chunk in split_file(ipath, 10000):
        with open(opath, 'w') as ofp:
            for doc in chunk:
                if 'title' not in doc or 'abstract' not in doc:
                    global drop_count
                    drop_count += 1
                    continue
                doc['title'] = doc['title'].lower().strip()
                doc['abstract'] = doc['abstract'].lower()
                doc['keywords'] = [e.lower().strip()
                                   for e in doc.get('keywords', [])],
                doc['fos'] = [e.lower().strip() for e in doc.get('fos', [])],
                json.dump({'index': {'_index': index}}, ofp)
                ofp.write('\n')
                json.dump(doc, ofp)
                ofp.write('\n')
        bulk_insert(index, opath)
    refresh(args.index)
    os.remove('tmp.json')


def main(args):
    """Entry point."""

    print(args)
    delete_index(args.index)
    create_index_aminer_v1(args.index)
    update_settings(args.index)
    inputs = sorted(args.inputs)
    for ipath in tqdm(inputs, total=len(inputs), unit='files'):
        index_worker(args.index, ipath)
    time.sleep(120)  # make sure that elasticsearch have time to refresh


if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    pparser.add_argument('--index', type=str, default='aminer_v1',
                         help='Name your data in Elasticsearch.')
    pparser.add_argument('--inputs', required=True, nargs='+',
                         help='Where is your data files?')
    args = pparser.parse_args()
    main(args)
    print('{} docs are dropped.'.format(drop_count))
