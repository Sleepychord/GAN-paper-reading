import re
import requests
import os

if not os.path.exists('./references'):
   os.makedirs('./references')
bib = open('sample.bib', 'r')
bigshot = ['Yann Lecun', 'Yoshua Bengio', 'Eric P. Xing', 'Ian J. Goodfellow', 'David Silver']
familiar = ['Zhilin Yang', 'Jun Zhu']

author_pattern = re.compile(r"author\s*=\s*{(.*?)},", re.S)
title_pattern = re.compile(r"title\s*=\s*{(.*?)},", re.S)
url_pattern = re.compile(r'url\s*=\s*{(.*?)},', re.S)
year_pattern = re.compile(r'year\s*=\s*{(.*?)}', re.S)

tot = 0
articles = bib.read().split('@article')
for article in articles:
   if len(article) > 10:
      name = ''
      year = year_pattern.search(article).group(1)
      name += year + ' '

      authors = author_pattern.search(article).group(1).split('and')
      a1 = authors[0].strip()
      a1 = re.sub('[^\w ]', '', a1)
      name += a1.split()[-1]

      has_bigshot = False
      for i in range(1, len(authors)):
         if(authors[i].strip() in bigshot or authors[i].strip() in familiar):
            has_bigshot = True
            name += '&' + authors[i].split()[-1]
      if not has_bigshot:
         name += ' et al'

      title = title_pattern.search(article).group(1)
      title = re.sub('[^\w\d:\- ]', '', title)
      name += ' ' + title + '.pdf'

      name = re.sub(' ', '-', ' '.join(name.split()))

      print name
      try:
         pdf = requests.get(url_pattern.search(article).group(1))    
         pdf.raise_for_status()
      except requests.RequestException as e:
          print(e)
      else:
         with open('./references/' + name, 'wb') as target:
            target.write(pdf.content)
      tot += 1
      print str(tot) + '/' + str(len(articles))

