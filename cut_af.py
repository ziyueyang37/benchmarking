import os
from Bio.PDB import PDBParser, PDBIO, Select, Chain
import pickle
import warnings
warnings.filterwarnings("ignore")

class ResidueSelection(Select):
    def __init__(self, res_num_to_keep):
        self.res_num_to_keep = res_num_to_keep

    def accept_residue(self, residue):
        return residue.get_id()[1] in self.res_num_to_keep


def renumber_residues(structure, residue_numbers_to_keep):
    selected_residues = ResidueSelection(residue_numbers_to_keep)
    #print(selected_residues)
    for model in structure:
        for chain in model.get_chains():
            new_chain = Chain.Chain(chain.get_id())
            #new_residues = []
            counter = 1
            for residue in chain:
                if selected_residues.accept_residue(residue):
                    new_residue = residue.copy()
                    new_residue.id = (residue.id[0], counter, residue.id[2])
                    new_chain.add(new_residue)
                    #new_residues[-1].id = (residue.id[0], counter, residue.id[2])
                    counter += 1
            #chain.detach_child_list()
            model.detach_child(chain.get_id())
            model.add(new_chain)
            #for new_residue in new_residues:
            #    chain.add(new_residue)


with open(f'afok_holo4k.pickle', 'rb') as handle:
    okdict = pickle.load(handle)

for pdbfile in os.listdir('./af/af_fixed_holo4k'):
    pdbid = pdbfile.split('.')[0]
    parser = PDBParser()
    structure = parser.get_structure('protein', f'./af/af_fixed_holo4k/{pdbfile}')
    try:
        res_start, res_end  = okdict[pdbid]
        res_num_to_keep = [i for i in range(res_start+1, res_end+1)]

        renumber_residues(structure, res_num_to_keep)

        io = PDBIO()
        io.set_structure(structure)
        io.save(f'./af/af_correct_holo4k/{pdbfile}')

    except:
        try:
            os.system(f'cp af/alphafold_holo4k_pdb/{pdbid}/ranked_0.pdb af/af_run_holo4k/{pdbid}.pdb')
        except:
            print(f'{pdbid} does not present')
            pass

