import os
from scipy.linalg import orthogonal_procrustes
import MDAnalysis as mda
import numpy as np
import pandas as pd
import warnings
import argparse
import pdbfixer
from simtk.openmm import app

warnings.filterwarnings("ignore")
# construct a mapping matrix from ESM to Crystal struct

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--dataset', type=str, required=True)

args = parser.parse_args()

data_list = os.listdir(f"./{args.model}/{args.model}_fixed_{args.dataset}")
result_dir = "./"
for filename in os.listdir(f'./{args.dataset}_ligand'):
    pdbid = filename.split("_")[0]
    file = open(f'./{args.dataset}_monomer_list.txt', 'r')
    data = file.read()
    monomer_list = data.split('\n')

    if pdbid not in monomer_list:
        continue
    if pdbid + ".pdb" not in data_list:
        continue
    print(pdbid)
    path_to_pdb = f'./{args.model}/{args.model}_fixed_{args.dataset}/' + pdbid + '.pdb'
    path_to_raw_data = f'./{args.dataset}_ligand/' + filename + '/protein.pdb'
    path_to_ligand = f'./{args.dataset}_ligand/' + filename + '/ligand.mol2'
    path_to_site = f'{args.dataset}_ligand/' + filename + '/site.mol2'
    fixer = pdbfixer.PDBFixer(filename=path_to_raw_data)
    fixer.findMissingResidues()
    fixer.findNonstandardResidues()
    fixer.replaceNonstandardResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    app.pdbfile.PDBFile.writeFile(fixer.topology, fixer.positions, open(f'./{args.dataset}_ligand/{filename}/protein_fixed.pdb', 'w'))
    path_to_data = f'./{args.dataset}_ligand/{filename}/protein_fixed.pdb'
    prdt = mda.Universe(path_to_pdb)
    cytl = mda.Universe(path_to_data)
    ligand = mda.Universe(path_to_ligand)
    site = mda.Universe(path_to_site)
    #prdt resnum always starts from 1
    prdt_res0 = prdt.residues[0].resid
    cytl_res0 = cytl.residues[0].resid
    diff = cytl_res0 - prdt_res0
    if (site.residues.resids[-1] - diff) >= len(prdt.residues):
        print('something wrong')
        continue

    prdt_site = prdt.residues[site.residues.resids - diff - 1].atoms.select_atoms('backbone')

    cytl_site = cytl.residues[site.residues.resids - diff - 1].atoms.select_atoms('backbone')
    if len(prdt_site) != len(cytl_site):
        print("length not same")
        print(prdt.residues[site.residues.resids - diff - 1])
        print(cytl.residues[site.residues.resids - diff - 1])
        continue
    prdt_pts = []
    cytl_pts = []
    for atom in prdt_site.atoms:
        prdt_pts.append(atom.position)
    for atom in cytl_site.atoms:
        cytl_pts.append(atom.position)

    transform_mat = orthogonal_procrustes(prdt_pts, cytl_pts)[0]
    #print(transform_mat) 
    p2rank = pd.read_csv(f"./p2rank_result/{args.model}_{args.dataset}/{pdbid}.pdb_predictions.csv")
    for i in range(len(p2rank)):
        binding_point = [p2rank["   center_x"][i], p2rank["   center_y"][i], p2rank["   center_z"][i]]
        mapped_point = binding_point @ transform_mat

        for atom in ligand.atoms:
            if np.sqrt(np.sum((atom.position - mapped_point)**2)) < 5: 
                print("yes")
                break    
