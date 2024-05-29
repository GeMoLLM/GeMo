import argparse
from openai import AzureOpenAI
import numpy as np
from tqdm import tqdm
import os.path as osp
import openai
import time

parser = argparse.ArgumentParser()
parser.add_argument('--input_id', type=str, default='codeonly')
parser.add_argument('--idx_fileid', type=str, default='')
args = parser.parse_args()

folder = '/scratch/fanw6/code_contests/'
input_filename = osp.join(folder, 'codeforces_A_file_paths_final.txt')
train_idx_filename = osp.join(folder, f'codeforces_A_gen_gpt-4{args.idx_fileid}_index.npy')

file_paths = []
with open(input_filename, 'r') as f:
    for line in f:
        file_paths.append(line.strip())
assert len(file_paths) == 100, f'len(file_paths)={len(file_paths)}'

train_idx = np.load(train_idx_filename)

client = AzureOpenAI(
    api_key=API_KEY,  
    api_version="2023-12-01-preview",
    azure_endpoint = "https://monoculture.openai.azure.com/"
)
deployment_name = 'monoculture-gpt-4-0125'

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model=deployment_name, # model = "deployment_name".
            messages=[
                {"role": "system", "content": "Assistant is a code language model capable of understanding and analyzing complicated competitive programming code."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except openai.RateLimitError as e:
        print("Rate limit exceeded, retrying in 10 seconds...")
        time.sleep(10)
        return generate_response(prompt)    

instruction = "Please read the following code and infer the algorithms and data structures used in it.\n"\
"For algorithms, select (a few) from the following list: \n"\
"\"Sorting Algorithms, Searching Algorithms, String Algorithms, Divide and Conquer Algorithms, Greedy Algorithms, Dynamic Programming, Recursion, Bit Manipulation, Backtracking, Graph Algorithms, Others\"\n"\
"For data structures, select (a few) from the following list: \n"\
"\"Arrays, Linked Lists, Stacks, Queues, Trees, Heaps, Hash Tables, Sets, Maps, Priority Queues, Others\"\n"\
"Answer each in a line following the format of: 'Algorithms: candidate 1, candidiate 2, ..\\nData structures: candidate 1, candidiate 2, ..\\n'\n"
print(instruction)

for file_path, indices in tqdm(zip(file_paths, train_idx)):
    fileid = file_path.split('_')[0]
    pid = file_path.split('_')[-1].split('.')[0]
    
    for i in tqdm(indices):
        file_path = osp.join(folder, f'{fileid}_solution_{args.input_id}_{i}_{pid}.py')

        lines = open(file_path).readlines()
        code = ''.join(lines)

        prompt = instruction + code
            
        output = generate_response(prompt)

        outfile_name = osp.join(folder, f'alg_ds_gpt-4_{fileid}_{pid}_gpt-4_{args.input_id}_{i}.txt')
        with open(outfile_name, 'w') as f:
            f.write(output)