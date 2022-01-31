import os
import glob
import pandas as pd

# Raw data
raw_data = './data/knowledge_en.csv'
raw_data_df = pd.read_csv(raw_data)
print(f'Raw data: {raw_data_df.shape[0]}')

# Translated data
trans_data_es_path = './data/translated_text_es/*.csv'
trans_data_fr_path = './data/translated_text_fr/*.csv'

for i in glob.glob(trans_data_es_path):
    i_th_df = pd.read_csv(i)
    print(f'Size of {os.path.basename(i)}: {i_th_df.shape[0]}')

for j in glob.glob(trans_data_fr_path):
    j_th_df = pd.read_csv(j)
    print(f'Size of {os.path.basename(j)}: {j_th_df.shape[0]}')


# Merged data
merge_path = './data/translated_merged_dfs/*.csv'
for k in glob.glob(merge_path):
    k_th_df = pd.read_csv(k)
    print(f'Size of {os.path.basename(k)}: {k_th_df.shape[0]}')

