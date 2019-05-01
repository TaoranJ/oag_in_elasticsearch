#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import argparse

import pandas as pd

from mag_schema import affiliations_header, authors_header
from mag_schema import conference_instances_header, conference_series_header
from mag_schema import fields_of_study_header, journals_header
from mag_schema import paper_author_affiliations_header
from mag_schema import paper_references_header, paper_resources_header
from mag_schema import paper_urls_header, papers_header

schema = {'Affiliations.txt': affiliations_header,
          'Authors.txt': authors_header,
          'ConferenceInstances.txt': conference_instances_header,
          'ConferenceSeries.txt': conference_series_header,
          'FieldsOfStudy.txt': fields_of_study_header,
          'Journals.txt': journals_header,
          'PaperAuthorAffiliations.txt': paper_author_affiliations_header,
          'PaperReferences.txt': paper_references_header,
          'PaperResources.txt': paper_resources_header,
          'Papers.txt': papers_header, 'PaperUrls.txt': paper_urls_header}

# Data table to be converted to JSON format
schema2json = {'Affiliations.txt': affiliations_header,
               'Authors.txt': authors_header,
               'ConferenceInstances.txt': conference_instances_header,
               'ConferenceSeries.txt': conference_series_header,
               'FieldsOfStudy.txt': fields_of_study_header,
               'Journals.txt': journals_header,
               'PaperResources.txt': paper_resources_header,
               'Papers.txt': papers_header, 'PaperUrls.txt': paper_urls_header}


def main(data_path, output):
    for table, header in schema2json.items():
        ipath = os.path.join(data_path, table)
        opath = os.path.join(output, table.replace('.txt', '.json'))
        chunks = pd.read_csv(ipath, sep='\t', quoting=3, lineterminator='\n',
                             chunksize=50000, header=None, names=header)
        with open(opath, 'w') as ofp:
            for chunk in chunks:
                for index, record in chunk.to_dict(orient='index').items():
                    record = {key: value.strip()
                              if type(value) is str else value
                              for key, value in record.items()}
                    json.dump(record, ofp)
                    ofp.write('\n')


if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    pparser.add_argument('--data-path', required=True,
                         help='Input data directory')
    pparser.add_argument('--output', required=True, help='Output directory')
    args = pparser.parse_args()
    main(args.data_path, args.output)
