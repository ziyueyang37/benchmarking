from schrodinger.structure import StructureReader
import os

for complex in os.listdir('/Users/yang1/psp/holo4k_ligand/'):
    ligand_path = '/Users/yang1/psp/holo4k_ligand/' + complex + '/ligand.mol2'
    try:
        struct = StructureReader.read(ligand_path)
        struct.write('/Users/yang1/psp/holo4k_ligand/' + complex + '/ligand_fix.mol2')
    except:
        print(complex)
        continue

