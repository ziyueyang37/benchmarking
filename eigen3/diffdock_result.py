import utils
import os
import pickle
import MDAnalysis as mda
import pandas as pd
import numpy as np

def run(model):
    dist_dict = {}
    with open('diffdock_af_holo4k.pickle', 'rb') as handle:
        resnum_dict = pickle.load(handle)
    #print(resnum_dict)
    for complex_id in resnum_dict.keys():
        pdbid = complex_id.split('_')[0]
        if model == 'diffdock':
            #print(resnum_dict)
            try:
                resnum = resnum_dict[complex_id]
            except:
                print(f'no result for {complex_id}')
                continue
            if f'{pdbid}.pdb' not in os.listdir('./data/af_all_holo4k'):
                continue 
            out = utils.mapping(complex_id, 'af', 'holo4k')
            #except:
            #    print('something is wrong')
            #    continue
            if out is 0:
                print(f'cannot compute transformation matrix for {complex_id}')
                continue
            mat, offset = out
        
        reslist = [ele-1 for ele in resnum]
        site = mda.Universe(f'./data/holo4k_ligand/{complex_id}/site.mol2')
        site_pt = np.average(site.residues.atoms.select_atoms('backbone').positions, axis=0)
        prdt = mda.Universe(f'./data/af_all_holo4k/{pdbid}.pdb')
        try:
            prdt_site = prdt.residues[reslist].atoms.select_atoms('backbone')
        except:
            print("Wrong")
            pass
        prdt_pt =  np.average(prdt_site.positions, axis=0)
         
        dist = np.sqrt(np.sum((prdt_pt @ mat - site_pt - offset)**2))
        dist_dict[complex_id] = dist    
        print(complex_id)
    with open(f'{model}_dist_af_holo4k.pickle', 'wb') as handle:
        pickle.dump(dist_dict, handle)
       
    return dist_dict

run('diffdock')
