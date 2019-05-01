#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

MAG dataset downloaded from Azure server follows the data schema document:
https://docs.microsoft.com/en-us/academic-services/graph/reference-data-schema.

"""

affiliations_header = ['AffiliationId', 'Rank', 'NormalizedName',
                       'DisplayName', 'GridId', 'OfficialPage',
                       'WikiPage', 'PaperCount', 'CitationCount',
                       'CreatedDate']

authors_header = ['AuthorId', 'Rank', 'NormalizedName', 'DisplayName',
                  'LastKnownAffiliationId', 'PaperCount', 'CitationCount',
                  'CreatedDate']

conference_instances_header = ['ConferenceInstanceId', 'NormalizedName',
                               'DisplayName', 'ConferenceSeriesId', 'Location',
                               'OfficialUrl', 'StartDate', 'EndDate',
                               'AbstractRegistrationDate',
                               'SubmissionDeadlineDate', 'NotificationDueDate',
                               'FinalVersionDueDate', 'PaperCount',
                               'CitationCount', 'CreatedDate']

conference_series_header = ['ConferenceSeriesId', 'Rank', 'NormalizedName',
                            'DisplayName', 'PaperCount', 'CitationCount',
                            'CreatedDate']

fields_of_study_header = ['FieldOfStudyId', 'Rank', 'NormalizedName',
                          'DisplayName', 'MainType', 'Level', 'PaperCount',
                          'CitationCount', 'CreatedDate']

journals_header = ['JournalId', 'Rank', 'NormalizedName', 'DisplayName',
                   'Issn', 'Publisher', 'Webpage', 'PaperCount',
                   'CitationCount', 'CreatedDate']

paper_author_affiliations_header = ['PaperId', 'AuthorId', 'AffiliationId',
                                    'AuthorSequenceNumber', 'OriginalAuthor',
                                    'OriginalAffiliation']

paper_references_header = ['PaperId', 'PaperReferenceId']

paper_resources_header = ['PaperId', 'ResourceType', 'ResourceUrl',
                          'SourceUrl', 'RelationshipType']

paper_urls_header = ['PaperId', 'SourceType', 'SourceUrl']

papers_header = ['PaperId', 'Rank', 'Doi', 'DocType', 'PaperTitle',
                 'OriginalTitle', 'BookTitle', 'Year', 'Date', 'Publisher',
                 'JournalId', 'ConferenceSeriesId', 'ConferenceInstanceId',
                 'Volume', 'Issue', 'FirstPage', 'LastPage', 'ReferenceCount',
                 'CitationCount', 'EstimatedCitation', 'OriginalVenue',
                 'CreatedDate']
