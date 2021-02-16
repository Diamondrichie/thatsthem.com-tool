import pprint
import requests
from bs4 import BeautifulSoup as bs

class Skipper:
    def __init__(self):
        self.fields = ['Phone Number', 'Alternate Phones', 'Email Address', 'Length of Residence', 
                'Household Size', 'IP Address', 'Estimated Net Worth', 'Estimated Income', 'Education',
                'Occupation', 'Language', 'Wealth Score', 'Green Score', 'Donor Score', 'Travel Score',
                'Tech Score', 'Shopping Score', 'Name', 'Address', 'Age']
        self.main()

    @staticmethod
    def get_text(element):
        if element:
            return element[-1].text if element[-1].text else '-'
        else:
            return '-'

    def find_skiper_data(self, record):
        dds = record.select('dd')
        dts = record.select('dt')
        dictionary = {dt.text.strip(): dd.text.strip() for dt, dd in zip(dts, dds)}

        name = self.get_text(record.select('span[itemprop="name"]'))
        dictionary['Name'] = name
        # fish out the address
        address = self.get_text(record.select('span[itemprop="streetAddress"]')) 
        locality = self.get_text(record.select('span[itemprop="addressLocality"]')) 
        region = self.get_text(record.select('span[itemprop="addressRegion"]'))
        postal__code = self.get_text(record.select('span[itemprop="postalCode"]'))
        address = ' '.join([address, locality, region, postal__code])
        dictionary['Address'] = address
        # # skipers age
        age = self.get_text(record.select('.ThatsThem-record-age .active'))
        dictionary['Age'] = age
        pprint.pprint(dictionary)
        return dictionary

    def make_request(self, name):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1ua.ff'}
        name = name.replace(' ', '-')
        res = requests.get("https://thatsthem.com/name/" + name, headers=headers)
        if res.ok:
            soup = bs(res.text, features="html.parser")
            records = soup.select(".ThatsThem-record")
            # for record in records:
            record = records[0]
            response = self.find_skiper_data(record)
            return response
        else:
            print(res.reason)

    def write_headings(self):
        self.fp = open('thatsthem.csv', 'w')
        headings = ','.join(self.fields)
        self.fp.write(headings + '\n')

    def write_data(self, dictionary):	
        values = ','.join([ dictionary.get(field) for field in self.fields])
        self.fp.write(values + '\n')

    def main(self):
        self.write_headings()
        r = self.make_request('jean doe')
        self.write_data(r)
        self.fp.close()
    