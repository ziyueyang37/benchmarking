import os
import pandas as pd
import MDAnalysis as mda
import numpy as np
import pickle
import glob
from scipy.linalg import orthogonal_procrustes


def read_p2rank(path):
    '''
    path to csv /Users/yang1/psp/p2rank_result/esm_holo4k/1dr3.pdb_residues.csv
    '''
    p2rank = pd.read_csv(path)
    resnums = []
    site_pts = []
    pdbid = path.split('.')[-3][-4:]
    setting = path.split('/')[-2]
    model = setting.split('_')[0]
    dataset = setting.split('_')[1]
    u = mda.Universe(f'./{model}/{model}_all_{dataset}/{pdbid}.pdb')
    for i in range(len(p2rank)):
        resnum = [int(ele.split('_')[-1]) for ele in p2rank[' residue_ids'][i].split(' ')[1:]]
        resnums.append(resnum)
        bb = u.residues[resnum].atoms.select_atoms('backbone')
        site_pts.append(np.average(bb.positions, axis=0))        
            
    return site_pts, resnums


def read_sitemap(path, pdbid):
    '''
    path to pickle ./resid_sitemap_esm_holo4k.pickle
    '''
    with open(path, 'rb') as handle:
        resdict = pickle.load(handle)
 
    reslist = resdict[pdbid]
    model = path.split('.')[-2].split('_')[-2]
    dataset = path.split('.')[-2].split('_')[-1]
    u = mda.Universe(f'./{model}/{model}_all_{dataset}/{pdbid}.pdb')
    resnums = []
    site_pts = []
    for record in reslist:
        numstr = record.split(': ')[-1]
        resnum = [int(ele) for ele in numstr.split(',')]
        resnums.append(resnum)
        bb = u.residues[resnum].atoms.select_atoms('backbone')
        site_pts.append(np.average(bb.positions, axis=0))
                
    return site_pts, resnums



def mapping(complex_id, model, dataset):
    '''
    complex_id in format '1anu_0'
    '''
    pdbid = complex_id.split('_')[0]
    path_to_pdb = f'./{model}/{model}_all_{dataset}/{pdbid}.pdb'  # generated structure
    path_to_data = f'./{dataset}_ligand/{complex_id}/protein.pdb'  # crystal structure
    path_to_site = f'./{dataset}_ligand/{complex_id}/site.mol2'  # crystal structure
    
    prdt = mda.Universe(path_to_pdb)
    cytl = mda.Universe(path_to_data)
    site = mda.Universe(path_to_site)
    print(complex_id)
    prdt_res0 = prdt.residues[0].resid
    cytl_res0 = cytl.residues[0].resid
    diff = cytl_res0 - prdt_res0
    #cytl_site = cytl.residues[site.residues.resids - diff - 1].atoms.select_atoms('backbone')
    #origin_site = site.residues.atoms.select_atoms('backbone')
    #print(cytl_site.positions == origin_site.positions)
    max_res_len = len(prdt.residues)
    try:
        prdt_site = prdt.residues[site.residues.resids - diff - 1].atoms.select_atoms('backbone')
        cytl_site = cytl.residues[:max_res_len][site.residues.resids - diff - 1].atoms.select_atoms('backbone')
        #origin_site = site.residues.atoms.select_atoms('backbone')
        #print(origin_site == cytl_site)
    except:
        print('residue index out of range')
        return 0
    prdt_pts = []
    cytl_pts = []
    for atom in prdt_site.atoms:
        prdt_pts.append(atom.position)
    for atom in cytl_site.atoms:
        cytl_pts.append(atom.position)

    try: 
        transform_mat = orthogonal_procrustes(prdt_pts, cytl_pts)[0]
        transform_offset = (np.average(prdt_pts, axis=0) @ transform_mat - np.average(cytl_pts, axis=0))
        #print(prdt_pts @ transform_mat - cytl_pts - transform_offset)
        return (transform_mat, transform_offset)
    except: 
        print('somwthing is wrong')
        return 0


def projection(dist_dict, complex_id, predict_reslists, predict_pts, mat, offset):
    '''
    given pdbid, transform the result from p2rank and sitemap to dataset space, 
    finding the possible site by ranking the resid overlap,
    each site return a dist
    '''
    complex_path = f'./holo4k_ligand/{complex_id}'
    
    site = mda.Universe(f'{complex_path}/site.mol2')
    site_pt = np.average(site.residues.atoms.select_atoms('backbone').positions, axis=0)
    site_reslist = site.residues.resids
    try:
        match_site = predict_reslists[0]
        match_pt = predict_pts[0]
    except:
        print('failed to predict and site')
        return dist_dict
    overlap_num = 0
    for predict_reslist, predict_pt in zip(predict_reslists, predict_pts):
        cur_overlap_num = len(set(site_reslist) & set(predict_reslist))
        if cur_overlap_num > overlap_num:
            overlap_num = cur_overlap_num
            match_site = predict_reslist
            match_pt = predict_pt
    print(overlap_num) 
    dist = np.sqrt(np.sum((match_pt @ mat - site_pt - offset)**2))
    dist_dict[complex_id] = dist
    
    return dist_dict
