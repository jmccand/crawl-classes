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

def get_cache(path, filename):
    html = None
    full_name = f'{cache_dir}{filename}'
    if os.path.exists(full_name):
        with open(full_name, 'rb') as f:
            html = f.read()
    else:
        html_obj = requests.get(path)
        with open(full_name, 'wb') as f:
            html = html_obj.content
            f.write(html)
    assert not html == None
    return html

pf = 0
cof = 0
clf = 0
for page_num in range(1, 21):
    catalog_html = get_cache(f'https://catalog.rpi.edu/content.php?catoid=24&navoid=606&filter%5Bcpage%5D={page_num}', f'cached_{page_num}.html')
    cat_soup = BeautifulSoup(catalog_html, 'html.parser')
    for class_link in cat_soup.find_all('a', href=True):
        if class_link['href'].startswith('preview_course'):
            m = re.search(r'catoid=(\d+)\&coid=(\d+)', class_link['href'])
            gs = m.groups()
            class_html = get_cache(f'https://catalog.rpi.edu/ajax/preview_course.php?catoid={gs[0]}&coid={gs[1]}&link_text=&show', f'{gs[0]}_{gs[1]}.html')
            class_soup = BeautifulSoup(class_html, 'html.parser')
            higher_td = class_soup.find('td', {'class': 'coursepadding'})
            central_div = higher_td.findChildren('div', recursive=False)[1]
            cdivtext = unicodedata.normalize('NFKD', str(central_div))
            header = central_div.findChildren('h3')[0].get_text()
            c, t = header.split(' - ')
            d = re.search(r'<hr\/>(.*?)(<br\/>|<\/p>)', cdivtext)
            dw = ''
            if not d is None:
                dw = d.groups()[0]
            p_ = cdivtext.lower().count('prereq')
            p = re.search(r'Prerequisis?tes?(:| -| or Other Requirements:| for undergraduates:) *(<a.*>(.*)<\/a>.*)+', cdivtext)
            pw = []
            if p is None:
                if p_ > 1:
                    pf += 1
            else:
                pw = [p.groups()[-1]]
            co = re.search(r'(C|c)orequisites?(:| -| )( Students in| PHYS 1500,)?(<\/strong>)? *(<a.*>(.*)<\/a>.*)+', cdivtext)
            co_ = cdivtext.lower().count('coreq')
            cow = []
            if co is None:
                if co_ > 1:
                    cof += 1
            else:
                cow = [co.groups()[-1]]
            cl = re.search(r'Cross Listed:<\/strong> (Cross listed with|Crosslisted with|Crossed with|With|Cross listed as|Cross-listed as|Cross-listed with|Cross listed)? ?(<a.*>(.*)<\/a>.*)+', cdivtext)
            if cl is None:
                if 'cross listed' in cdivtext.lower():
                    clf += 1
            course_dict[c] = Course(c, t, dw, pw, cow)

# print(list(c.codes for c in course_dict.values()))
print(f'prereqs parse success percentage: {1 - pf/len(course_dict)}')
print(f'coreqs parse success percentage: {1 - cof/len(course_dict)}')
print(f'cross listed parse success percentage: {1 - clf/len(course_dict)}')
with open(wfile, 'wb') as f:
    f.write(pickle.dumps(course_dict))
