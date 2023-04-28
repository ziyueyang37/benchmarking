import pdbfixer
import os
from simtk.openmm import app

with open('./holo4k_monomer_list.txt', 'r') as f:
    data = f.read()
    pdblist = data.split('\n')

idx = 0
for esm_struct in os.listdir('./esm/esm_structs'):
    if esm_struct[-8:-4] in pdblist:
        print(idx)
        fixer = pdbfixer.PDBFixer(filename='./esm/esm_structs/'+esm_struct)
        fixer.findMissingResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
        app.pdbfile.PDBFile.writeFile(fixer.topology, fixer.positions, open("./esm_fixed/"+esm_struct[-8:-4]+".pdb", 'w'))
        idx += 1
