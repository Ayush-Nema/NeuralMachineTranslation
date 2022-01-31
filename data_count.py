"""
Counts the number of utterances in each subintent
"""
import pandas as pd

data = pd.read_csv('data/knowledge_en.csv')
df = data.groupby('subintent')['utterance'].count()
df0 = data.groupby('subintent')['utterance'].nunique()
print(df)
