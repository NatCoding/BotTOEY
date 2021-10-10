import requests
import re

from requests.api import head
def counter_hero(hero):
    if " " in hero:
        hero = hero.replace(" ","-")
        url='https://www.dotabuff.com/heroes/{}'.format(hero)
        r = requests.get(url,headers={'user-agent': 'Mozilla/5.0'})
        html = r.text
        section = re.search(r'<section><header>Worst Versus.+?</section>', html).group()
        headers = re.findall(r'<th[^>]*>([^<]+)', section)
        rows = re.findall(r'<td>(?:<a[^>]*>)?([^<]+)', section)
    else:
        pass
        url='https://www.dotabuff.com/heroes/{}'.format(hero)
        r = requests.get(url,headers={'user-agent': 'Mozilla/5.0'})
        html = r.text
        section = re.search(r'<section><header>Worst Versus.+?</section>', html).group()
        headers = re.findall(r'<th[^>]*>([^<]+)', section)
        rows = re.findall(r'<td>(?:<a[^>]*>)?([^<]+)', section)
    return rows