import csv
import os
import argparse

'''
based on pdb_id
1. iterate over folders in _ligand data
2. see if the pdb_id is in monomer list
3. if yes, point pdb path to generated dataset, point ligand path to the crystal dataset
'''

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--dataset', type=str, required=True)
args = parser.parse_args()

monomer_list = open('./' + args.dataset + '_monomer_list.txt').read().split('\n')
path_dict_list = []
for filename in os.listdir('./data/' + args.dataset + '_ligand/'):
    #print(filename)
    pdbid = filename.split('_')[0]
    if pdbid not in monomer_list:
        continue
    #if pdbid in ['1ats','1ize', '4z9l','1i76']:
    if pdbid + '.pdb' not in os.listdir('./data/pprep_pdb_{0}_{1}/'.format(args.model, args.dataset)):
        continue
    if filename+'.sdf' in os.listdir('./diffdock/results_{0}_{1}/all/'.format(args.model, args.dataset)):
        print("Already exist, skip!")
        continue
    path_dict = {}
    #path_dict['protein_path'] = f'./data/{args.model}_all_{args.dataset}/{pdbid}.pdb'
    #path_dict['protein_path'] = './data/{0}_all_{1}/{2}.pdb'.format(args.model, args.dataset, pdbid)
    path_dict['protein_path'] = './data/pprep_pdb_' + args.model + '_' + args.dataset + '/' + pdbid + '.pdb'
    path_dict['ligand'] = './data/' + args.dataset + '_ligand/' + filename + '/charged_ligand.sdf'
    path_dict_list.append(path_dict)

fields = ['protein_path', 'ligand']
with open('diffdock_path_{0}_{1}.csv'.format(args.model, args.dataset), 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames = fields)
    writer.writeheader()
    writer.writerows(path_dict_list) 
