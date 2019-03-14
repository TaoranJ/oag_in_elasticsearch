# -*- coding: utf-8 -*-

import os
import json
import pickle
from collections import defaultdict

import elasticsearch
import elasticsearch.helpers
import pandas as pd
import matplotlib.pyplot as plt


def _draw_fos_total_hits(opath, fos_hits_year, min_year, max_year):
    """Draw fos total hits by year.

    Parameters
    ----------
    opath : str
        Output directory.
    fos_hits_year : dict
        Fos' Total hits by year.
    min_year : int
        Min year to consider.
    max_year : int
        Max year to consider.

    """

    if not os.path.exists(opath):
        os.makedirs(opath)
    for tech, hits in fos_hits_year.items():
        hits_by_year = sorted([(y, h) for y, h in hits.items()
                               if y >= min_year and y <= max_year],
                              key=lambda k: k[0])
        if hits_by_year:
            x, y = zip(*hits_by_year)
            fig = plt.figure()
            plt.plot(x, y)
            plt.xlim(min_year, max_year)
            fig.savefig(os.path.join(opath, tech.replace('/', '_') + '.png'))
            plt.close()


class MAG(object):
    def __init__(self, *, query_file, output_dir, index, min_year, max_year):
        super(MAG, self).__init__()
        if query_file:
            self.query_file = os.path.basename(query_file).replace('.json', '')
            self.queries = set([q.lower().strip()
                               for q in json.load(open(query_file, 'r'))])
        self.opath = output_dir
        self.es = elasticsearch.Elasticsearch()
        self.index = index
        if min_year and max_year:
            self.min_year, self.max_year = min_year, max_year

    def fos_total_hits_analysis(self):
        """Distribution of fos total hits."""

        fos_hits_all = {}
        fos_hits_year = defaultdict(lambda: defaultdict(lambda: 0))
        for ix, query in enumerate(self.queries, start=1):
            query_es = {'query': {'match_phrase': {'fos.keyword': query}}}
            total_hits = self.es.count(index=self.index,
                                       body=query_es)['count']
            if total_hits <= 0:
                continue
            fos_hits_all[query] = total_hits
            hits = elasticsearch.helpers.scan(self.es, index=self.index,
                                              query=query_es)
            for count, hit in enumerate(hits, start=1):
                fos_hits_year[query][hit['_source']['year']] += 1
            assert(total_hits == count)
            print('[Done query ... {:04d}/{:04d}]'.format(ix,
                                                          len(self.queries)))
        # analysis on total hits of each query
        opath = os.path.join(self.opath, 'fos_total_hits')
        if not os.path.exists(opath):
            os.makedirs(opath)
        plt.plot(sorted(list(fos_hits_all.values()), reverse=True))
        plt.savefig(os.path.join(opath, self.query_file + '.png'), dpi=600)
        total_hits = pd.DataFrame.from_dict(fos_hits_all, orient='index',
                                            columns=['total_hits'])
        total_hits.to_csv(os.path.join(opath, self.query_file + '.csv'),
                          index_label='index')
        print(total_hits.describe())
        # analysis on total hits by year
        opath = os.path.join(opath, 'by_year')
        _draw_fos_total_hits(opath, fos_hits_year, self.min_year,
                             self.max_year)

    def fos_subdataset_gen(self):
        """Get sub dataset given a list of queries (e.g. "deep learning",
        "machine learning")"""

        pids = set()
        opath = os.path.join(self.opath, self.query_file + '.json')
        with open(opath, 'w') as ofp:
            for ix, query in enumerate(self.queries, start=1):
                print('[BATCH {:03d}/{:03d}]'.format(ix, len(self.queries)))
                query = {'query': {'match_phrase': {
                    'fos.keyword': query.strip()}}}
                res = elasticsearch.helpers.scan(self.es, index='mag_v1',
                                                 query=query,
                                                 request_timeout=30)
                for data in res:
                    pid = data['_id']
                    if pid not in pids:
                        pids.add(pid)
                        json.dump({'id': pid, **data['_source']}, ofp)
                        ofp.write('\n')

    def keyword_gen(self, input_path, max_len=4):
        opath = os.path.join(self.opath, 'keywords')
        if not os.path.exists(opath):
            os.makedirs(opath)
        opath_anno = os.path.join(
                opath, os.path.basename(input_path).replace('.json', '')
                + '.annotation')
        opath_dict = os.path.join(
                opath, os.path.basename(input_path).replace('.json', '')
                + '.dictionary')
        dictionary, annotation = set(), {}
        with open(input_path, 'r') as ifp:
            for paper in ifp:
                paper = json.loads(paper)
                dictionary, annotation = self._keyword(
                        paper.get('keywords', []), dictionary, annotation,
                        max_len)
                dictionary, annotation = self._fos(
                        paper.get('fos', []), dictionary, annotation,
                        max_len)
        pickle.dump(dictionary, open(opath_dict, 'wb'))
        pickle.dump(annotation, open(opath_anno, 'wb'))

    def _keyword(self, keywords, dictionary, annotation, max_len):
        """Collect keywords from mag dataset.

        Parameters
        ----------
        keywords: list
            List of keywords in mag paper.
        dictionary: set
            Set of keywords.
        annotation: dict
            Dictionary of annotations.
        max_len:
            Max length.

        Returns
        -------
        dictionary: set
            Set of keywords.
        annotation: dict
            Dictionary of annotation like {"deep_learning": "deep learning"}

        """

        for keyword in keywords:
            lens = len(keyword.split())
            if lens > max_len:
                continue
            anno = ''.join([c if c.isalnum() else '_' for c in keyword])
            if lens > 1 and anno not in annotation:
                annotation[keyword] = anno
            dictionary.add(anno)
        return dictionary, annotation

    def _fos(self, foss, dictionary, annotation, max_len):
        """Collect fos from mag dataset.

        Parameters
        ----------
        foss: list
            List of fos in mag paper.
        dictionary: set
            Set of keywords.
        annotation: dict
            Dictionary of annotations.
        max_len:
            Max length.

        Returns
        -------
        dictionary: set
            Set of keywords.
        annotation: dict
            Dictionary of annotation like {"deep_learning": "deep learning"}

        """

        for fos in foss:
            lens = len(fos.split())
            if lens > max_len:
                continue
            anno = ''.join([c if c.isalnum() else '_' for c in fos])
            if lens > 1 and anno not in annotation:
                annotation[fos] = anno
            dictionary.add(anno)
        return dictionary, annotation
