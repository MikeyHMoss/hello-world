## Attempting to create dataframe of members of UK Parliament
## Code should find list of members elected, navigate to their wiki page and collect some data on them.

from bs4 import BeautifulSoup, SoupStrainer
import urllib
import pandas as pd
import re

# Gets the right rows of information by providing criteria to the soup parser
url = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_United_Kingdom_general_election,_2017').read()
parse_mp_entries = SoupStrainer(attrs={"vcard"})
soup = BeautifulSoup(url,"html.parser", parse_only=parse_mp_entries)

# loops through each item parsed and extracts the shortened link then creates the string for the full url
mp_links = list()
for link in soup.find_all('a'):
        mp_links.append('https://en.wikipedia.org'+str(link.get('href')))

#Now we need to navigate to each MP's page and collect their data
for i in mp_links:
    url = urllib.request.urlopen(i).read()
    political_soup = BeautifulSoup(url,"html.parser")
    # Now we have navigated to the page, we get the data.

    # First, the name of the politician
    name = political_soup.find('h1').get_text()

    # Second, take the text of their description across the article and join it into a single variable
    desc_list = list()
    for i in political_soup.find_all('p'):
        desc_list.append(i.get_text())
    description = " ".join(desc_list)

    # Now take the political party, the constituency, and their majority in votes and share.
    # The date of birth and the constituency are found via tag navigation
    info_box = political_soup.find(attrs={"infobox"})
    info_box_text = info_box.get_text()

    constituency = info_box.find(href=re.compile("UK_Parliament_constituency")).string
    if info_box.find(attrs={"class":"bday"}):
        d_o_b = info_box.find(attrs={"class":"bday"}).string
    elif re.search('Born\n(\d+)',info_box_text):
        d_o_b = re.search('Born\n(\d+)',info_box_text).group(1)
    else:
        d_o_b = None

    # With no viable tagging, other variables are found through a regex
    if re.search('Majority\n(\d+,?\d+?)',info_box_text):
        majority_string = re.search('Majority\n(\d+,?\d+?)',info_box_text).group(1)
        majority_number = int(majority_string.replace(",",""))
    else:
        majority_number = None


    if re.search('\(?(\d+\.?\d+?)', info_box_text):
        majority_perc_string = re.search('\(?(\d+\.?\d+?)', info_box_text).group(1)
        majority_perc = float(majority_perc_string)
    else:
        majority_perc = None

    if re.search('Political\sparty\n(.+)',info_box_text):
        political_party = re.search('Political\sparty\n(.+)',info_box_text).group(1)
    else:
        political_party = None

    # Now we create the data frame
    row = [(name, political_party, constituency, description, d_o_b, majority_number, majority_perc)]
    labels = ['name','political_party','constituency','description', 'd_o_b', 'majority_number', 'majority_perc']
    df_row = pd.DataFrame(data=row, columns=labels)
    try:
        df.append(df_row)
    except:
        df = df_row
    print('finished with ' + name)

print(df)
