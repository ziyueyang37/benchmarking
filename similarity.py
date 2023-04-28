import os
import MDAnalysis as mda
import nglview as nv
import numpy as np
import math

pdbid = '1g8o'
path_to_pdb = './esm/esm_structs/' + pdbid + '.pdb'
path_to_data = './dataset/' + pdbid + '/protein.pdb'
path_to_site = './dataset/' + pdbid + '/site.mol2'
path_to_site0 = './dataset/' + pdbid + '/site_for_ligand_0.mol2'

prdt = mda.Universe(path_to_pdb)
cytl = mda.Universe(path_to_data)
site = mda.Universe(path_to_site)
site0 = mda.Universe(path_to_site0)

prdt_select = prdt.select_atoms("resid 53:60")
for slct_res in select.residues:
    print(slct_res)
prdt_pts = []
for atom in select.atoms:
    print(atom)
    prdt_pts.append(atom.position)

cytl_select = cytl.select_atoms("resid 133:140 and not name H*")
for slct_res in cytl_select.residues:
    print(slct_res)
cytl_pts = []
for atom in cytl_select.atoms:
    print(atom)
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
print(mat1)
print(mat2)
