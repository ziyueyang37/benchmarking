import pandas as pd
import MDAnalysis as mda
import numpy as np
import pickle
import utils
import os

def run(model):
    dist_dict = {}
    for complex_id in os.listdir('./holo4k_ligand'):
        pdbid = complex_id.split('_')[0]
        if model == 'p2rank':
            try:
                pts, nums = utils.read_p2rank(f'/Users/yang1/psp/p2rank_result/af_holo4k/{pdbid}.pdb_predictions.csv')
            except:
                print('skip this one')
                continue
        elif model == 'sitemap':
            try:
                pts, nums = utils.read_sitemap('./sitemap_resnum_af_holo4k.pickle', pdbid)
            except:
                print('skip this one')
                continue
        else: 
            print('invalid input')
            break

        out = utils.mapping(complex_id, 'af', 'holo4k')
        if out is 0:
            print(f'cannot compute transformation matrix for {complex_id}')
            continue
        mat, offset = out
        dist_dict = utils.projection(dist_dict, complex_id, nums, pts, mat, offset)
    with open(f'some_result_{model}_af_holo4k.pickle', 'wb') as handle:
        pickle.dump(dist_dict, handle)
    return dist_dict

