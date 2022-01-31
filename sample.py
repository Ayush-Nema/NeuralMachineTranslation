import pandas as pd
from tqdm import trange
from transformers import MarianTokenizer, AutoModelForSeq2SeqLM

# Reading the dataframe
en_utts = pd.read_csv("data/knowledge_en.csv")
en_utts = en_utts.utterance

mname = 'Helsinki-NLP/opus-mt-en-fr'
tokenizer = MarianTokenizer.from_pretrained(mname)
model = AutoModelForSeq2SeqLM.from_pretrained(mname)

text = ['Hi, I am RNN, the father of NLP', 'where is Alabama located', 'when is the next match of Kolkata Knight '
                                                                       'Riders']

for i in trange(len(text)):
    input_ids = tokenizer.encode(text[i], return_tensors="pt")
    outputs = model.generate(input_ids)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(decoded)

