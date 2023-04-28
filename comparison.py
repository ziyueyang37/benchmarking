import os
import MDAnalysis as mda
import nglview as nv
import math
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--dataset', type=str, required=True)

args = parser.parse_args()

print(args.dataset)
gen_dir = f"./{args.model}/{args.model}_all_{args.dataset}/"


data_dir = f'./{args.dataset}_ligand/'
mono_list = f'./{args.dataset}_monomer_list.txt'

result = {}
gen_list = os.listdir(gen_dir)
for filename in os.listdir(data_dir):
    pdbid = filename.split("_")[0]
    file = open(mono_list, 'r')
    data = file.read()
    monomer_list = data.split('\n')
    
    if pdbid not in monomer_list:
    # or pdbid in ['1jb9','1trq','1f9u','1mgp','1tio','1f9v','1m13','1db1','1ie8', '1kpm','1ie9','1lzj','1ddg','1jsv','1fdr','1n3z','1lij','1i7g','1nsa','1g55','1jt1','1ke8','1n6a']:
        continue
    if pdbid + ".pdb" not in gen_list:
        continue
    print(pdbid)
    path_to_pdb = gen_dir + pdbid + '.pdb'
    path_to_data = data_dir + filename + '/protein.pdb'
    path_to_site = data_dir + filename + '/site.mol2'
    try: 
        prdt = mda.Universe(path_to_pdb)
    except:
        print(pdbid)
        continue
    cytl = mda.Universe(path_to_data)
    site = mda.Universe(path_to_site)

    #prdt resnum always starts from 1
    prdt_res0 = prdt.residues[0].resid
    cytl_res0 = cytl.residues[0].resid
    #print(prdt_res0)
    #print(cytl_res0)
    diff = cytl_res0 - prdt_res0
    #diff = cytl.residues.resids[:len(prdt.residues)] - prdt.residues.resids  
    if (site.residues.resids[-1] - diff - 1) >= len(prdt.residues):
        continue
    prdt_site = prdt.residues[site.residues.resids - diff - 1].atoms.select_atoms('backbone')
    #print(len(prdt_site))
    cytl_site = cytl.residues[site.residues.resids - diff - 1].atoms.select_atoms('backbone')
    #print(len(cytl_site))
    if len(prdt_site) != len(cytl_site):
        continue
    prdt_pts = []
    cytl_pts = []
    for atom in prdt_site.atoms:
        prdt_pts.append(atom.position)
    for atom in cytl_site.atoms:
        cytl_pts.append(atom.position)

    def lcl_strct_cmpr(pts1, pts2):
        '''
        compare the similarity of two point clouds
        pts1 -- list of xyz coords
        pts2 -- list of xyz coords
        len(pts1) == len(pts2)
        '''
        adj_mat1 = np.zeros((len(pts1), len(pts1)))
        adj_mat2 = np.zeros((len(pts2), len(pts2)))
        for i, pt11 in enumerate(pts1):
            for j, pt12 in enumerate(pts1):
                adj_mat1[i,j] = math.dist(pt11, pt12)
            
        for i, pt21 in enumerate(pts2):
            for j, pt22 in enumerate(pts2):
                adj_mat2[i,j] = math.dist(pt21, pt22)
        return adj_mat1, adj_mat2 
    
    mat1, mat2 = lcl_strct_cmpr(cytl_pts, prdt_pts)
    rmsd = np.sqrt(np.sum((mat1 - mat2)**2)) / (len(mat1)**2)
    if rmsd > 0.0375:
        print(rmsd)
    result[filename] = rmsd

with open('rmsd_{0}_{1}.pickle'.format(args.model, args.dataset), 'wb') as pkl:
    pickle.dump(result, pkl)
