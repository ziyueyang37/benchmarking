import os
import uuid
import shutil
import traceback

import sys
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--dataset', type=str, required=True)
args = parser.parse_args()

#PPREP_FOLDER = f"./pprep_{args.model}_{args.dataset}"
PPREP_FOLDER = f"./af/{args.model}_all_{args.dataset}"

def template_run_script(pdb_id):
    schrodinger = os.environ['SCHRODINGER']
    cwd = os.getcwd()
    cmd = [
        f"{schrodinger}/sitemap",
        '-grid', str(0.7),  # 0.7 by default for both RBSS and SiteMap
        '-nthresh', str(7),  # 7 by default for RBSS and 3 by default for SiteMap
        '-dthresh', str(3.5),  # 3.5 by default for RBSS and 6.5 by default for SiteMap
        '-d2thresh', str(3.0),  # 3.0 by default for RBSS and 3.1 by default for SiteMap
        "-j", str(uuid.uuid4()),
        '-prot', f"{cwd}/{pdb_id}.pdb",
        '-writepot', 'yes',
        '-writegrids', 'yes'
    ]
    return cmd


def run_bash(args):
    retval = subprocess.run(args,
                            capture_output=True)
    print(retval.stdout.decode("utf-8"))
    print(retval.stderr.decode("utf-8"))


def change_directory_and_run(pdb_id):
    cur_dir = os.getcwd()
    try:
        os.chdir(f"sitemap/{args.model}_{args.dataset}/{pdb_id}")
        cmd = template_run_script(pdb_id)
        print(cmd)
        run_bash(cmd)
    except Exception as e:
        traceback.print_exc()
    finally:
        os.chdir(cur_dir)


def run_sitemap(pdb_mae):
    pdb_id = os.path.splitext(pdb_mae)[0]
    os.makedirs(f"sitemap/{args.model}_{args.dataset}/{pdb_id}", exist_ok=True)
    shutil.copy(f'{PPREP_FOLDER}/{pdb_mae}', f'sitemap/{args.model}_{args.dataset}/{pdb_id}/{pdb_mae}')
    change_directory_and_run(pdb_id)


def main():
    pdb_ids = os.listdir(PPREP_FOLDER)
    pdb_maes = [x for x in pdb_ids if x.endswith(".pdb")]
    for pdb_mae in pdb_maes:
        run_sitemap(pdb_mae)


if __name__ == "__main__":
    if 'SCHRODINGER' not in os.environ:
        print("Must have Schrodinger Specified")
        sys.exit(1)
    main()
