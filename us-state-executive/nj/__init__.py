from pupa.scrape import Jurisdiction
from .executive import NJGovernorPressScraper

import re


class NJGovernorScraper(Jurisdiction):
    jurisdiction_id = 'ocd-jurisdiction/country:us/state:nj'
    name = 'New Jersey State Governor'
    url = 'http://www.state.nj.us/governor/'
    terms = [
        {'name': '1962-1970',
         'sessions': ['Richard_J_Hughes'],
         'start_year': 1962,
         'end_year': 1970},
        {'name': '1974-1982',
         'sessions': ['Brendan_Byrne'],
         'start_year': 1974,
         'end_year': 1982},
        {'name': '1990-1994',
         'sessions': ['James_J_Florio'],
         'start_year': 1990,
         'end_year': 1994},
        {'name': '1994-2001',
         'sessions': ['Christine_Todd_Whitman'],
         'start_year': 1994,
         'end_year': 2001},
        {'name': '2001-2002',
         'sessions': ['Donald_T_DiFrancesco'],
         'start_year': 2001,
         'end_year': 2002},
        {'name': '2002-2002',
         'sessions': ['John_O_Bennett', 'Richard_J_Codey_', 'John_Farmer_Jr'],
         'start_year': 2002,
         'end_year': 2002},
        {'name': '2002-2004',
         'sessions': ['James_E_McGreevey'],
         'start_year': 2002,
         'end_year': 2004},
        {'name': '2004-2006',
         'sessions': ['Richard_J_Codey'],
         'start_year': 2004,
         'end_year': 2006},
        {'name': '2006-2010',
         'sessions': ['Jon_S_Corzine'],
         'start_year': 2006,
         'end_year': 2010},
        {'name': '2010-2014',
         'sessions': ['Chris_Christie'],
         'start_year': 2010,
         'end_year': 2014}
    ]
    provides = ['events']
    session_details = dict()
    for t in terms:
        for s in t['sessions']:
            session_details.update({s: {'_scraped_name': s,
                                        'display_name': ' '.join(
                                            [re.sub('_', ' ', s).strip(), ''.join(['(', t['name'], ')'])])}})

    def get_scraper(self, term, session, scraper_type):
        if scraper_type == 'events':
            return NJGovernorPressScraper

    def scrape_session_list(self):
        return [s['_scraped_name'] for s in self.session_details.itervalues()]