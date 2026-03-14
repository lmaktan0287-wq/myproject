import requests
from bs4 import BeautifulSoup

url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops'
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print('=== Pagination ===')
for sel in ['li.next a', 'a[rel=next]', '.pagination a', 'ul.pagination a']:
    found = soup.select(sel)
    if found:
        print(f'FOUND: {sel}')
        for f in found:
            print(' ', f)

print('=== Next button HTML ===')
pag = soup.select('.pagination')
for p in pag:
    print(p)