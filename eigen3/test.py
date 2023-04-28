from rdkit import Chem
from openbabel import openbabel
from openbabel import pybel
import os
import re

def fix_ligand(obmol):
    #obmol.addh()
    obmol.OBMol.PerceiveBondOrders()
    for atom in obmol.atoms:
        bondnum = 0
        for neighbour_atom in openbabel.OBAtomAtomIter(atom.OBAtom):
            #print(neighbour_atom.GetAtomicNum())
            bond = atom.OBAtom.GetBond(neighbour_atom)
            #print(bond.GetBondOrder())
            bondnum += bond.GetBondOrder()
        #atomtype = list(atom.type)[0]
        try:
            number = re.findall(r'\d+', atom.type)[0]
            #print(number)
            atomtype = atom.type.split(number)[0]
        except:
            if atom.type in ['Cl', 'Be', 'Br']:
                atomtype = atom.type
            else:
                atomtype = list(atom.type)[0]
        #print(atom.type)
        #print(atomtype)
        #print(bondnum)
        if atomtype == "C":
            charge = bondnum - 4
        elif atomtype == "N":
            charge = bondnum - 3
        elif atomtype == "O":
            charge = bondnum - 2
        elif atomtype == "Cl":
            charge = bondnum - 1
        elif atomtype == "Be":
            charge = 2 - bondnum
        elif atomtype == "Mg":
            charge = 2 - bondnum
        elif atomtype == "B":
            charge = bondnum - 5
        else:
            charge = 0
        #print(charge)
        atom.OBAtom.SetFormalCharge(charge)
    return obmol

for complexes in os.listdir('./data/coach420_ligand/'):
    #if complexes != '1jep_1':
    #    continue
    obmol = next(pybel.readfile('mol2', './data/coach420_ligand/' + complexes + '/ligand.mol2'))
    #print(obmol.molwt)
    obmol = fix_ligand(obmol)
# Define the SMILES string
#smiles_string = 'N1=[C+](=O)NC(=O)C(N2)C1N(C(C=23)=CC(C)=C(C)C3=O)CC(O)C(O)C(O)COP([O-])(=O)OP([O-])(=O)OCC4C(O)C(O)C(O4)n(cn5)c(c56)ncnc6N'
    #obmol.write("mol2", "./data/holo4k_ligand/" + complexes + "/charged_ligand.mol2", overwrite=True)
    ligand_file = "./data/coach420_ligand/" + complexes + "/charged_ligand.sdf"
    #rdkitmol = Chem.rdmolfiles.MolFromMol2File(ligand_file)    
    #if rdkitmol is None:
    #    print("Invalid mol2 file")
    
    smiles_string = obmol.write("smiles")
    failed_complexes = []
    print(smiles_string) 
    try:
        mol = Chem.MolFromSmiles(smiles_string)
        #if mol is None:
        #    print("Invalid SMILES string")
        #else:
        #    print("SMILES string parsed successfully")
        with Chem.SDWriter(ligand_file) as w:
            w.write(mol)
    except: 
        failed_complexes.append(complexes)
        print(complexes)
with open('failed_complexes.txt', 'w') as f:
    f.writelines(failed_complexes)
