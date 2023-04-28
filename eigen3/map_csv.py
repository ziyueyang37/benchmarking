import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--dataset', type=str, required=True)
args = parser.parse_args()


batch_size = 20
df = pd.read_csv(f'./diffdock_path_{args.model}_{args.dataset}.csv')
for i in range(0, len(df), batch_size):
    df_batched = pd.DataFrame(df.iloc[i:i+batch_size, :], columns=['protein_path', 'ligand'])
    df_batched.to_csv(os.path.join(f'./diffdock/map_{args.model}_{args.dataset}/', f"map_{i//batch_size}.csv"), index=False)
