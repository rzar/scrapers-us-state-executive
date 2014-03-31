from pupa.scrape import Jurisdiction
from .executive import NYGovernorPressScraper

import re


class NYGovernorScraper(Jurisdiction):
    jurisdiction_id = 'ocd-jurisdiction/country:us/state:ny'
    name = 'New York State Governor'
    url = 'http://www.governor.ny.gov/'
    terms = [{
        'name': '2011-2014',
        'sessions': ['Andrew_M_Cuomo'],
        'start_year': 2011,
        'end_year': 2014
    }]
    provides = ['events']
    parties = [
        {'name': 'Democratic'}
    ]

    def get_scraper(self, term, session, scraper_type):
        if scraper_type == 'events':
            return NYGovernorPressScraper

    session_details = dict()
    for t in terms:
        for s in t['sessions']:
            session_details.update({s: {'_scraped_name': s,
                                        'display_name': ' '.join(
                                            [re.sub('_', ' ', s).strip(), ''.join(['(', t['name'], ')'])])}})

    def scrape_session_list(self):
        return [s['_scraped_name'] for s in self.session_details.itervalues()]