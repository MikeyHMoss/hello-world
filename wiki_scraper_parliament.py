## the current version of this isn't working
## Attempting to create dataframe of members of UK Parliament
## Code should find list of members elected, navigate to their wiki page and collect some data on them.

import time
from bs4 import BeautifulSoup, SoupStrainer
import urllib
import pandas as pd
import re
import csv

start_time = time.time()
# Gets the right rows of information by providing criteria to the soup parser
url = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_United_Kingdom_general_election,_2017')
entries = url.read()
url.close()
parse_mp_entries = SoupStrainer(attrs={"vcard"})
soup = BeautifulSoup(entries,"html.parser", parse_only=parse_mp_entries)

# loops through each item parsed and extracts the shortened link then creates the string for the full url

mp_links = list()
for link in soup.find_all('a'):
        mp_links.append('https://en.wikipedia.org'+str(link.get('href')))

# #trim the links in order to test
# mp_links_test = mp_links[0:5]

#Now we need to navigate to each MP's page and collect their data
data_list = []
for i in mp_links:
    url = urllib.request.urlopen(i)
    data = url.read()
    url.close()
    political_soup = BeautifulSoup(data,"html.parser")
    link = str(i)

    # Get the name
    name = political_soup.find('h1').get_text()
    name = re.sub('\(.+\)','',name)

    # Second, take the text of their description across the article and join it into a single variable
    desc_list = list()
    for par in political_soup.find_all('p'):
        desc_list.append(par.get_text())
    description = " ".join(desc_list)
    description = re.sub('\[.+\]','',description)

    ## Now take the political party, the constituency, and their majority in votes and share.

    # The date of birth and the constituency are found via tag navigation
    info_box = political_soup.find(attrs={"infobox"})
    info_box_text = info_box.get_text()

    # Get the political party
    parties = ['Labour', 'Conservative', 'Liberal Democrat','Scottish Nationalist Party', 'Plaid Cymru','Sinn Féin', 'Independent', 'Green']
    if re.search('Political\sparty\n(.+)',info_box_text):
        political_party = re.search('Political\sparty\n(.+)',info_box_text).group(1)
        # political_party = [x for x in parties if x == parties]
    else:
        political_party = None

    # Get the date of birth
    if info_box.find(attrs={"class":"bday"}):
        d_o_b = info_box.find(attrs={"class":"bday"}).string
    elif re.search('Born\n(\d+)',info_box_text):
        d_o_b = re.search('Born\n(\d+)',info_box_text).group(1)
    else:
        d_o_b = None

    # Get the constituency
    constituency = info_box.find(href=re.compile("UK_Parliament_constituency")).string

    # Get the majority as an int and %
    if re.search('Majority\n',info_box_text):
        majority = re.search('Majority\n(.+)\n', info_box_text).group(1)
        majority = re.split('\s', majority)
        majority_num = int(re.sub('[^\d]','',majority[0]))
        try:
            majority_perc = float(re.sub('[^\d\.]','',majority[1]))
            if majority_perc < 100.0:
                majority_perc = majority_perc
            else:
                majority_perc = None
        except:
            majority_perc = None
    else:
        majority_num = None
        majority_per = None

    data_row = {'name':name,
                'constituency': constituency,
                'desc': description,
                'political party': political_party,
                'date of birth': d_o_b,
                'majority': majority_num,
                '%majority' : majority_perc,
                'link': link
                }
    data_list.append(data_row)

df = pd.DataFrame(data_list)
df.to_csv('HoC_data.csv')
elapsed_time = time.time() - start_time
print(elapsed_time)
