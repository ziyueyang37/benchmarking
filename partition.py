from bs4 import BeautifulSoup
import requests
import re
from urllib.request import urlopen
import os

Monomers = []
for pdbid in os.listdir('./coach420'):
    if pdbid == '1pmq':
        pdbid = '4z9l'
    if pdbid == '1fpx':
        pdbid = '6cig'
    if pdbid == '1m98':
        pdbid = '5ui2'
    url = "https://www.rcsb.org/structure/" + pdbid[:-1]
    print(url)
    r = requests.get(url)
    if r.status_code != 200:
        continue 
    soup = BeautifulSoup(r.content)
    mydivs = soup.find_all(class_="carousel-footer")
    for tag in mydivs[1]():
        tag.decompose()
    if mydivs[1].get_text()[-10:-3] == 'Monomer':
        #print(pdbid)
        Monomers.append(pdbid)
with open('./coach420_monomer_list.txt', 'w') as f:
    f.write('\n'.join(Monomers))
print(len(Monomers))
