import os
import rdkit
from rdkit import Chem
from Bio.PDB import PDBParser, PDBIO
from Bio.PDB import Atom, Residue, Chain
from Bio.PDB import NeighborSearch
import pickle

def mol_to_residue(mol, chain_id="L", res_num=1):
    residue = Residue.Residue((' ', res_num, ' '), 'LIG', ' ')
    #, mol.GetProp("_Name"), ' ')
    conf = mol.GetConformer()
    for atom in mol.GetAtoms():
        atom_name = atom.GetSymbol() + str(atom.GetIdx())
        atom_coord = conf.GetAtomPosition(atom.GetIdx())
        try:
            new_atom = Atom.Atom(atom_name, atom_coord, 0.0, 0.0, " ", atom_name, atom.GetIdx(), element=atom.GetSymbol())
        except:
            new_atom = Atom.Atom(atom_name, atom_coord, 0.0, 0.0, " ", atom_name, atom.GetIdx(), element='X')
        residue.add(new_atom)
    chain = Chain.Chain(chain_id)
    chain.add(residue)
    return chain


def write_complex(complex_id, model, dataset):
    # read protein PDB file
    pdbid = complex_id.split('_')[0]
    ligand_file = f'./diffdock/results_{model}_{dataset}/all/{complex_id}.sdf/rank1.sdf' 
    protein_file = f'./data/{model}_all_{dataset}/{pdbid}.pdb'
    parser = PDBParser()
    try:
        structure = parser.get_structure("protein", protein_file)
    except:
        print('target protein file doesnot exist')
        pass
    # read ligand SDF file
    try:
        ligand_supplier = Chem.SDMolSupplier(ligand_file)
    except:
        print('no diffdock result for this complex')
        pass
    ligand_mol = ligand_supplier[0]
    
    ligand_chain = mol_to_residue(ligand_mol)
     
    # add ligand chain to the protein structure
    structure[0].add(ligand_chain)

    # save the combined structure as a new PDB file
    io = PDBIO()
    io.set_structure(structure)
    io.save(f'./complex/{complex_id}_{model}_{dataset}.pdb')

    return structure


def find_binding_res(complex_id, model, dataset, threshold=5):
    '''
    complex_file --> .pdb # target protein (generated structures)
    '''
    complex_file = f'./complex/{complex_id}_{model}_{dataset}.pdb'
    parser = PDBParser()
    structure = parser.get_structure("protein-ligand_complex", complex_file)
    ligand_identifier = 'LIG'
    #for atom in structure.get_atoms():
        #print(atom.parent.resname)
    ligand_atoms = [atom for atom in structure.get_atoms() if atom.parent.resname == ligand_identifier]
    protein_atoms = [atom for atom in structure.get_atoms() if atom.parent.resname != ligand_identifier]
    
    # Find close residues
    neighbor_search = NeighborSearch(protein_atoms)
    close_residues = set()
    for ligand_atom in ligand_atoms:
        nearby_residues = neighbor_search.search(ligand_atom.coord, threshold)
        for residue in nearby_residues:
            #print(residue.parent.id)
            #print(residue.id)
            residue_id = residue.parent.id
            #+ residue.id[1]
            close_residues.add(residue_id[1])    
    #print(close_residues)
    return close_residues


def run(complex_id, model, dataset):
    #pdbid = complex_id.split('_')[0]
    write_complex(complex_id, model, dataset)
    close_residues = find_binding_res(complex_id, model, dataset)
    return close_residues


def loop(model, dataset):
    diffdock_dict = {}
    for complex_sdf in os.listdir(f'./diffdock/results_{model}_{dataset}/all'):
        complex_id = complex_sdf.split('.')[0]
        close_residues = run(complex_id, model, dataset)
        diffdock_dict[complex_id] = close_residues
        print(complex_id)
        print(close_residues)

    with open (f'diffdock_{model}_{dataset}.pickle', 'wb') as pkl:
        pickle.dump(diffdock_dict, pkl)

loop('af', 'holo4k')
