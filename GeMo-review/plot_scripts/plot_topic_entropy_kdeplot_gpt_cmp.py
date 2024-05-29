import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import argparse
import numpy as np
import os.path as osp
import os
import warnings
from scipy.stats import gaussian_kde
import colorsys
from plot_utils import get_shades, rgb_to_hex, read_data, \
    plot_stacked_barchart, plot_custom_barcharts, plot_kdeplot

TICK_SIZE = 30
plt.rc('xtick', labelsize=TICK_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=TICK_SIZE)    # fontsize of the tick labels
plt.rc('axes', labelsize=TICK_SIZE)
warnings.filterwarnings("ignore", category=UserWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--metric', type=str, default='entropy')
args = parser.parse_args()

folder = 'analysis_results_topic'
src_path = osp.join(folder, 'summary_topic_goodreads_src_grouped_reviews_long_sub_en_10.pkl')
gen_path_1 = osp.join(folder, f'summary_topic_goodreads_personalized_gpt-3.5-instruct-chat_500.pkl')
gen_path_2 = osp.join(folder, f'summary_topic_goodreads_personation_gpt-3.5-instruct-chat_500.pkl')
gen_path_3 = osp.join(folder, f'summary_topic_goodreads_personalized_gpt-4-chat_500.pkl')
gen_path_4 = osp.join(folder, f'summary_topic_goodreads_personation_gpt-4-chat_500.pkl')

sent_src = pickle.load(open(src_path, 'rb'))

books = list(sent_src.keys())
print(gen_path_1)
sent_x_src = read_data(src_path, books, args.metric)
sent_x_gen_1 = read_data(gen_path_1, books, args.metric)
sent_x_gen_2 = read_data(gen_path_2, books, args.metric)
sent_x_gen_3 = read_data(gen_path_3, books, args.metric)
sent_x_gen_4 = read_data(gen_path_4, books, args.metric)

T_list = 1.2
P_list = 1.0

out_folder = 'figs/'
os.makedirs(out_folder, exist_ok=True)

# Load the "Paired" palette
palette = sns.color_palette("Paired")
palette_set2 = sns.color_palette("Set2")

# Omit the first color, making the first in the list single, and then pairs follow
modified_palette = [palette_set2[0]] + palette[0:4]

data_list = [sent_x_src,
             [x for x in sent_x_gen_1[:,-1,-1] if x != -1],
             [x for x in sent_x_gen_2[:,-1,-1] if x != -1],
             [x for x in sent_x_gen_3[:,-1,-1] if x != -1],
             [x for x in sent_x_gen_4[:,-1,-1] if x != -1],
             ]

plot_kdeplot(
    data_list,
    f'fig_topic_histplot_{args.metric}_gpt_cmp.pdf', 
    colors=modified_palette,
    alpha=0.02
)