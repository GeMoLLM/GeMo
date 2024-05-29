import argparse
import numpy as np
from itertools import combinations
import json
from utils import jaccard_similarity_index, regularize_tags

parser = argparse.ArgumentParser()
parser.add_argument('--input_id', type=str, default='codeonly')
parser.add_argument('--model', type=str, default='gpt-3.5-instruct')
parser.add_argument('--model_fam', type=str, default='gpt4')
parser.add_argument('--idx_fileid', type=str, default='')
parser.add_argument('--input_filename', type=str, default='codeforces_A_file_paths_final.txt')
args = parser.parse_args()

input_filename = f'./{args.input_filename}'
train_idx_filename = f'codeforces_A_gen_{args.model_fam}{args.idx_fileid}_index.npy'

file_paths = []
with open(input_filename, 'r') as f:
    for line in f:
        file_paths.append(line.strip())
# assert len(file_paths) == 100, f'len(file_paths)={len(file_paths)}'

train_idx = np.load(train_idx_filename)

sim_scores = []

all_data = []
for file_path, indices in zip(file_paths, train_idx):
    fileid = file_path.split('_')[0]
    pid = file_path.split('_')[-1].split('.')[0]
    
    tags_list = []
    for i in indices:
        input_file = f'parsed_description_{args.model}_{fileid}_solution_{args.input_id}_{i}_{pid}.json'
        cur_tags = regularize_tags(json.load(open(input_file))['tags'].split(', '))
        all_data += cur_tags
        tags_list.append(set(list(np.unique(cur_tags))))
    
    similarity = jaccard_similarity_index(tags_list)
    sim_scores.append(similarity)
    print(f"similarity index: {similarity} of {fileid} {pid}")

print(np.unique(all_data))

out_file = f'tags_train_solution_similarity_gen_{args.input_id}_{args.model}_final.npy'
print(out_file)
np.save(out_file, np.array(sim_scores))