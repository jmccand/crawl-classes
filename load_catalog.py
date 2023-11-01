import requests
from bs4 import BeautifulSoup
import os
import re
import unicodedata
import pickle
from coursedef import Course


cache_dir = 'caches/'
course_dict = {}
wfile = 'catalog.pickle'

# get the existing cached page at this file
def get_cache(path, filename):
    html = None
    full_name = f'{cache_dir}{filename}'
    if os.path.exists(full_name):
        # open existing file
        with open(full_name, 'rb') as f:
            html = f.read()
    else:
        # get the html from requests
        html_obj = requests.get(path)
        with open(full_name, 'wb') as f:
            # save the html for next time
            html = html_obj.content
            f.write(html)
    assert not html == None
    return html

# parsing prerequisites fail count
pf = 0
# parsing corequisites fail count
cof = 0
# parsing cross list fail count
clf = 0
# go through each page in catalog
for page_num in range(1, 21):
    # get html for the page of courses
    catalog_html = get_cache(f'https://catalog.rpi.edu/content.php?catoid=24&navoid=606&filter%5Bcpage%5D={page_num}', f'cached_{page_num}.html')
    # set up catalog soup object
    cat_soup = BeautifulSoup(catalog_html, 'html.parser')
    # find all class links
    for class_link in cat_soup.find_all('a', href=True):
        # only links with preview course b/c
        # one preview course link per course
        if class_link['href'].startswith('preview_course'):
            # get catoid and coid
            m = re.search(r'catoid=(\d+)\&coid=(\d+)', class_link['href'])
            gs = m.groups()
            # get html for this course
            class_html = get_cache(f'https://catalog.rpi.edu/ajax/preview_course.php?catoid={gs[0]}&coid={gs[1]}&link_text=&show', f'{gs[0]}_{gs[1]}.html')
            # set up class soup object
            class_soup = BeautifulSoup(class_html, 'html.parser')

            # parse information
            # first td to find
            higher_td = class_soup.find('td', {'class': 'coursepadding'})
            # body of course in central div
            central_div = higher_td.findChildren('div', recursive=False)[1]
            # cdivtext is central div text
            cdivtext = unicodedata.normalize('NFKD', str(central_div))
            # find course header in central div
            header = central_div.findChildren('h3')[0].get_text()
            # course code (c), class title (t)
            c, t = header.split(' - ')
            # description regex match (d)
            d = re.search(r'<hr\/>(.*?)(<br\/>|<\/p>)', cdivtext)
            # description to be written (dw)
            dw = ''
            if not d is None:
                dw = d.groups()[0]
            # prerequisites count (p_)
            p_ = cdivtext.lower().count('prereq')
            # prerequisites regex match (p)
            p = re.search(r'Prerequisis?tes?(:| -| or Other Requirements:| for undergraduates:) *(<a.*?>(.*?)<\/a>)', cdivtext)
            # prerequisites to be written (pw)
            pw = []
            if p is None:
                if p_ > 1:
                    # at least one prerequisite for course but cannot be parsed
                    # increment fail counter
                    pf += 1
            else:
                # get the prerequisites from the regex groups
                pw = [p.groups()[-1]]
            # corequisites regex match (co)
            co = re.search(r'(C|c)orequisites?(:| -| )( Students in| PHYS 1500,)?(<\/strong>)? *(<a.*?>(.*?)<\/a>)', cdivtext)
            # corequisites count (co_)
            co_ = cdivtext.lower().count('coreq')
            # corequisites to be written (cow)
            cow = []
            if co is None:
                if co_ > 1:
                    # at least one corequisite for course but cannot be parsed
                    # increment fail counter
                    cof += 1
            else:
                # get the corequisites from the regex groups
                cow = [co.groups()[-1]]
            # cross linked (cl)
            cl = re.search(r'Cross Listed:<\/strong> (Cross listed with|Crosslisted with|Crossed with|With|Cross listed as|Cross-listed as|Cross-listed with|Cross listed)? ?(<a.*>(.*)<\/a>.*)+', cdivtext)
            if cl is None:
                if 'cross listed' in cdivtext.lower():
                    # at least one cross listed course but cannot be parsed
                    # increment fail counter
                    clf += 1
            # add to ourse dictionary
            course_dict[c] = Course(c, t, dw, pw, cow)

# print(list(c.codes for c in course_dict.values()))
print(f'prereqs parse success percentage: {1 - pf/len(course_dict)}')
print(f'coreqs parse success percentage: {1 - cof/len(course_dict)}')
print(f'cross listed parse success percentage: {1 - clf/len(course_dict)}')
# write pickle file of course dictionary
with open(wfile, 'wb') as f:
    f.write(pickle.dumps(course_dict))
