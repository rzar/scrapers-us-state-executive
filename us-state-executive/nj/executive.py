from pupa.scrape import Scraper
from pupa.models import Event

from mimetypes import MimeTypes
from lxml import html as lxml_html
import datetime as dt
import re


class NJGovernorPressScraper(Scraper):
    def get_events(self):
        # get list of executive orders
        url = 'http://nj.gov/infobank/circular/eoindex.htm'
        page = self.urlopen(url)
        page = lxml_html.fromstring(page)
        page.make_links_absolute(url)

        # state variables for parser
        governor_name = None
        gov_session_name = None

        # parse the table of executive orders
        for eo_row in page.xpath('//table[@border>0]//tr'):

            cols = eo_row.xpath('.//td')

            # extract governor's name
            if len(cols) == 1:
                # remove things like "'s"
                governor_name = re.sub('\W\w\s', ' ', eo_row.xpath('string()'))
                governor_name = re.sub('\\r*\\n|\W', ' ', governor_name)
                governor_name = re.sub('\s+', ' ', governor_name)
                governor_name = re.search("executive order.*governor(.*)administration",
                                          governor_name, re.IGNORECASE).groups()[0].strip()
                gov_session_name = re.sub('\s+', '_', governor_name)

            # extract executive order
            elif len(cols) == 3:
                if self.session == gov_session_name:
                    eo_num = cols[0].xpath('string()').strip()
                    try:
                        float(eo_num)
                    except ValueError:
                        continue

                    eo_title = re.sub('\\r*\\n', ' ', cols[1].xpath('string()'))
                    eo_title = re.sub('\s+', ' ', eo_title)
                    eo_title = re.sub('\[.*pdf.*\]', '', eo_title).strip()
                    if eo_title == '' or eo_title is None:
                        continue

                    eo_date = re.search('([0-9]{1,2}).*/([0-9]{1,2}).*/([0-9]{4}|[0-9]{2})', cols[2].xpath('string()'))
                    if eo_date is None:
                        continue
                    eo_date = '/'.join(eo_date.groups())
                    try:
                        eo_date = dt.datetime.strptime(eo_date, '%m/%d/%y')
                    except ValueError:
                        eo_date = dt.datetime.strptime(eo_date, '%m/%d/%Y')

                    eo_source = cols[0].xpath('.//a')[0].get('href').lower()
                    mime_type = MimeTypes().guess_type(eo_source)[0]
                    if mime_type is None:
                        mime_type = 'text/html'

                    # build yield object
                    eo = Event(eo_num, eo_date, 'New Jersey', gov_session_name)
                    eo.add_person(governor_name, 'governor')
                    eo.description = eo_title
                    eo.add_document(eo_num, eo_source, mime_type)
                    eo.add_source(eo_source)

                    yield eo