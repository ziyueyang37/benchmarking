import os
import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('--model', type=str, required=True)
#parser.add_argument('--dataset', type=str, required=True)
#args = parser.parse_args()
#model = args.model
#dataset = args.dataset
num_jobs = len(os.listdir(f'./diffdock/map_esm_coach420/')) 
for job in range(num_jobs):
    with open ('./workflow/run_{0}.sh'.format(job), 'w') as rsh:
        rsh.write('''\
#! /bin/bash
export job=%s
export protein_ligand_path="diffdock/map_esm_coach420/map_${job}.csv"
mkdir -p diffdock/results_esm_coach420/${job}
echo "PROCESSING ESM: ${protein_ligand_path}"
source activate diffdock-gpu
python DiffDock/datasets/esm_embedding_preparation.py \
--protein_ligand_csv ${protein_ligand_path} \
--out_file diffdock/data/prepared_for_esm.fasta

HOME=DiffDock/esm/model_weights
python DiffDock/esm/scripts/extract.py \
esm2_t33_650M_UR50D diffdock/data/prepared_for_esm.fasta \
diffdock/data/esm2_output_${job} --repr_layers 33 --include per_tok

# assign diffdock parameters whoever you decide
python DiffDock/inference.py --protein_ligand_csv ${protein_ligand_path} --out_dir diffdock/results_esm_coach420/${job} \
--inference_steps 20 --samples_per_complex 5 --batch_size 3 \
--actual_steps 18 --no_final_step_noise --cache_path diffdock/data/cache_${job} \
--esm_embeddings_path diffdock/data/esm2_output_${job} --model_dir DiffDock/workdir/paper_score_model \
--confidence_model_dir DiffDock/workdir/paper_confidence_model

rm -r diffdock/data/cache_${job}*
rm -r diffdock/data/esm2_output_${job}

# depending on the number
# of ligands, it's important to assign and then delete your cache path between runs or
# you'll run out of space
''' %(job))
