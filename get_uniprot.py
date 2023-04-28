from bs4 import BeautifulSoup
import requests
import re
from urllib.request import urlopen
import json
import os
import subprocess

f = open("coach420_monomer_list.txt", "r")
empty_entry_pdb = []
for pdbid in f.read().splitlines():
    #print(pdbid)
    pdb_mapping_url = 'https://www.rcsb.org/structure/{0}'.format(pdbid)
    #print(pdb_mapping_url)
    pdb_mapping_response = requests.get(pdb_mapping_url)
    #print(pdb_mapping_response)
    soup = BeautifulSoup(pdb_mapping_response.content, features="html.parser")
    mydivs = soup.find_all(target="_blank", rel="noopener")
    for ele in mydivs:
        if not "www.uniprot.org" in ele['href']: continue
        uniprot = ele.text
    if uniprot == '':
        empty_entry_pdb.append(pdbid)
        continue
    os.system("$SCHRODINGER/run -FROM psp af2_process.py {0}".format(uniprot))
    os.system("cp *.pdb ./af_struct_coach420/{0}.pdb".format(pdbid))
    os.system("rm -rf *.pdb")
    os.system("rm -rf *.mae")
    os.system("rm -rf *.json")
file = open('empty_entry_pdb.txt','w')
for item in empty_entry_pdb:
    file.write(item+"\n")
file.close()
