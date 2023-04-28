from schrodinger import structure
from Bio import Align
from Bio.Align import substitution_matrices
import os
import pickle

afok = []
afnotok = []
count = 0
dict = {}
for pdb in os.listdir('./af/af_fixed_coach420/'):
    pdbid = pdb.split('.')[0]
    if pdbid in ['4z9l','1ize']:
        continue
    print(pdbid)
    #read in pdb files (cannot use {pdb}_crystal.pdb)
    with structure.StructureReader(f'./esm/esm_all_coach420/{pdbid}.pdb') as reader:
        for st in reader:
            rec_rf = st
    with structure.StructureReader(f'./af/af_fixed_coach420/{pdbid}.pdb') as reader:
        for st in reader:
            rec_af = st

    #seq_rf = ''.join([r.getCode().upper() for r in rec_rf.chain['A'].residue if r.isStandardResidue()]) 
    seq_rf = ''.join([r.getCode().upper() for r in rec_rf.residue])
    seq_af = ''.join([r.getCode().upper() for r in rec_af.residue]) 

    aligner = Align.PairwiseAligner()
    aligner.mode = 'global'
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -1
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62") 

    result = (aligner.align(seq_rf, seq_af)[0].aligned)
    buck = [len(a) for a in result][0]
    if buck == 1:
        count += 1
        print(count)
        #print(result)
        diff = result[1][0][0] - result[0][0][0]
        dict[pdbid] = (result[1][0][0] - result[0][0][0], result[1][0][1])
        #print(dict[pdbid])
        afok.append(pdbid)
    else: afnotok.append(pdbid)

print(count)
#file = open('afok_coach420.txt', 'w')
#file.writelines(afok)
#file.close()

#file2 = open('afnotok_coach420.txt', 'w')
#file2.writelines(afnotok)
#file2.close()
#with open('afok_coach420.txt', 'w') as fp:
#    fp.write("\n".join(afok))

#with open('afnotok_holo4k.txt', 'w') as fp:
#    fp.write("\n".join(afnotok))

with open('afok_coach420.pickle', 'wb') as handle:
    pickle.dump(dict, handle)
