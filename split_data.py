import os
import command
import subprocess

for pdbid in os.listdir('./dataset'):
    count = subprocess.getoutput('ls -lR ./dataset/%s/*.sdf | wc -l' % pdbid)
    for idx in range(int(count)):
        os.system("mkdir ./holo4k_ligand/%s_%d" % (pdbid, idx))
        os.system("cp ./dataset/%s/protein.pdb ./holo4k_ligand/%s_%d/protein.pdb" % (pdbid, pdbid, idx))
        os.system("cp ./dataset/%s/site_for_ligand_%d.mol2 ./holo4k_ligand/%s_%d/site.mol2" % (pdbid, idx, pdbid, idx))
#print(os.system("pwd"))

#count = subprocess.getoutput('ls -lR ./*.sdf | wc -l')

