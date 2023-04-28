from schrodinger.structure import StructureReader
import glob
#import MDAnalysis as mda
import os
import pickle

resdict = {}
for pdbid in os.listdir('./sitemap/af_holo4k/'):
    filename = f"./sitemap/esm_holo4k/{pdbid}/*_out.maegz"
    
    try:
        maefile = glob.glob(filename)[0]
    except:
        continue
    reslist = []
    with StructureReader(maefile) as reader:
        for st in reader:
            try:
                reslist.append(st.property['s_sitemap_residues'])
            except:
                continue
    resdict[pdbid] = reslist

with open('sitemap_resnum_af_holo4k.pickle', 'wb') as handle:
    pickle.dump(resdict, handle)
