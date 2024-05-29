from transformers import pipeline
import argparse
import spacy
import os
import os.path as osp
import numpy as np
from tqdm import tqdm
import json
import umap.umap_ as UMAP
from bertopic import BERTopic
import pickle
from analyze_utils import read_in_texts

parser = argparse.ArgumentParser()
parser.add_argument('--T_list', type=str, default='0.5,0.8,1.0,1.2')
parser.add_argument('--P_list', type=str, default='0.90,0.95,0.98,1.00')
parser.add_argument('--model', type=str, default='llama-2-13b')
parser.add_argument('--mode', type=str, default='personalized')
parser.add_argument('--device', '-d', type=int, default=0)
args = parser.parse_args()

T_list = args.T_list.split(',')
P_list = args.P_list.split(',')
os.environ['TRANSFORMERS_CACHE'] = '../cache/huggingface/'
os.environ['CUDA_VISIBLE_DEVICES'] = str(args.device)

# prepare the indices_dict
indices_dict_path = f'indices_dict_goodreads_{args.mode}_{args.model}-chat_500.pkl'
indices_dict = pickle.load(open(indices_dict_path, 'rb'))
print('load in indices_dict!')

# load in the sentiment classifier
topic_model = BERTopic.load("MaartenGr/BERTopic_Wikipedia")
print('load in topic model!')

out_folder = 'results_topic'
os.makedirs(out_folder, exist_ok=True)

for T in T_list:
    for P in P_list:
        input_folder = f'folder_goodreads_completions_{args.mode}_{args.model}-chat_500_temp-{T}-p-{P}'

        files = os.listdir(input_folder)
        d_topic = {}
        for file in tqdm(files):
            file_path = osp.join(input_folder, file)
            texts = read_in_texts(
                file_path,  
                indices_dict[T][P][file.replace('.jsonl', '')])
            topics, scores = topic_model.transform(texts)
        
            d_topic[file] = list([int(x) for x in topics])
            
        out_file = f'{out_folder}/topic_goodreads_{args.mode}_{args.model}-chat_500_temp-{T}-p-{P}.json'
        print(out_file)
        json.dump(d_topic, open(out_file, 'w'))