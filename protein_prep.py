import os
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--dataset', type=str, required=True)

args = parser.parse_args()

def template_run_script(model, dataset, pdb_id):
    outdir = 'pprep0_' + model + '_' + dataset
    problem_set = model + '/' + model + '_all_' + dataset
    schrodinger = os.environ['SCHRODINGER']
    PDB_INFILE_BASE = "."
    pdb_file = f"{PDB_INFILE_BASE}/{problem_set}/{pdb_id}.pdb"
    #print(pdb_file)
    OUT_BASE = f"{PDB_INFILE_BASE}/{outdir}"
    pdb_code = pdb_id
    #os.path.splitext(pdb_id)[0]
    #print(os.system("pwd"))
    #print(pdb_code)
    mae_out = f"{OUT_BASE}/{pdb_code}.maegz"
    #print(mae_out)
    #CMD = [
    #    f"{schrodinger}/run",
    #    "prepwizard2_driver.py",
    #    f"{pdb_file}",
    #    f"{mae_out}",
    #    "-fillsidechains",
    #    "-disulfides",
    #    "-rehtreat",
    #    "-max_states", "1",
    #    "-epik_pH", "7.4",
    #    "-epik_pHt", "2.0",
    #    "-antibody_cdr_scheme", "Kabat",
    #    "-minimize_adj_h",
    #    "-propka_pH", "7.4",
    #    "-f", "S-OPLS",
    #    "-rmsd", "0.3",
    #    "-watdist", "5.0",
    #    "-HOST", "localhost"
    #]
    command = '$SCHRODINGER/run prepwizard2_driver.py {0} {1} -fillsidechains -disulfides -rehtreat -max_states 1 -epik_pH 7.4 -epik_pHt 2.0 -antibody_cdr_scheme Kabat -minimize_adj_h -propka_pH 7.4 -f S-OPLS -rmsd 0.3 -watdist 5.0'.format(pdb_file, mae_out)
    return command


def run_bash(args):
    #subprocess.run(args,
                            #capture_output=True,
    #               shell=True)
    #print(retval.stdout.decode("utf-8"))
    #print(retval.stderr.decode("utf-8"))
    os.system(args)

def main():
    #problem_set = args.model + '/' + args.model + '_fixed_' + args.dataset
    #pdb_ids = os.listdir(problem_set)
    #for pdb_id in pdb_ids:
    #    cmd = template_run_script(args.model, args.dataset, pdb_id[-8:-4])
    #    run_bash(cmd)
    outdir = 'pprep0_' + args.model + '_' + args.dataset
    exist_pdbs = os.listdir(outdir)
    problem_set = args.model + '/' + args.model + '_all_' + args.dataset
    pdb_ids = os.listdir(problem_set)
    job_pdbs = [i for i in pdb_ids if i[-8:-4] + '.maegz' not in exist_pdbs]
    idx = 0
    for pdb_id in job_pdbs:
        #idx += 1
        #print(idx)
        cmd = template_run_script(args.model, args.dataset, pdb_id[-8:-4])
        run_bash(cmd)


if __name__ == "__main__":
    if 'SCHRODINGER' not in os.environ:
        print("Must have Schrodinger Specified")
        sys.exit(1)
    main()
