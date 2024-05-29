import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import argparse
import numpy as np
import os.path as osp
import os
import warnings
from analyze_utils import calculate_counter_similarity

warnings.filterwarnings("ignore", category=UserWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='llama-2-13b')
parser.add_argument('--mode', type=str, default='personalized')
args = parser.parse_args()

folder = 'analysis_results_wordfreq'
src_path = osp.join(folder, 'summary_wordfreq_goodreads_src_grouped_reviews_long_sub_en_10.pkl')
gen_path = osp.join(folder, f'summary_wordfreq_goodreads_{args.mode}_{args.model}-chat_500.pkl')

src_data = pickle.load(open(src_path, 'rb'))
gen_data = pickle.load(open(gen_path, 'rb'))

src_counter = src_data

T_list = [0.5, 0.8, 1.0, 1.2]
P_list = [0.90, 0.95, 0.98, 1.00]

out_folder = 'tables'
os.makedirs(out_folder, exist_ok=True)

sim = np.zeros((4, 4))
for ti, T in enumerate(T_list):
    for pi, P in enumerate(P_list):
        gen_counter = gen_data[T][P]
        sim[ti][pi] = calculate_counter_similarity(src_counter, gen_counter)

np.save(f'{out_folder}/wordfreq_cossim_{args.mode}_{args.model}-chat_500.npy', sim)