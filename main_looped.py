import sys
import time
import pandas as pd
from tqdm import trange
from transformers import MarianTokenizer, AutoModelForSeq2SeqLM
from utilities.utility import init_cmd_args

# Parsing the command line arguments
cmd_args = init_cmd_args(sys.argv[1:])

# Reading the dataframe
data = pd.read_csv(cmd_args.data_path)
df0 = data.groupby('subintent').nunique()
all_idx = df0.index.to_list()

# Sub-setting the data based on subintent if `subset` CLI argument is passed
if cmd_args.subset is not None:
    data = data[data['subintent'] == cmd_args.subset]


# Loading the pre-trained model
if cmd_args.translate == 'en_fr':
    mname = 'Helsinki-NLP/opus-mt-en-fr'
else:
    mname = 'Helsinki-NLP/opus-mt-en-es'

# Initialising the pre-trained model
tokenizer = MarianTokenizer.from_pretrained(mname)
model = AutoModelForSeq2SeqLM.from_pretrained(mname)


def translator(text):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(input_ids)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded


if __name__ == '__main__':
    start = time.perf_counter()

    trans_text, trans_subint = [], []
    for subint in all_idx:
        subset_data = data[data['subintent'] == subint]
        en_utts, subintents = subset_data.utterance, subset_data.subintent
        print(f'Initialising translation for {subint} subintent')

        for i in trange(len(en_utts)):
            ith_utt = translator(en_utts.iloc[i])
            trans_text.append(ith_utt)
            trans_subint.append(subintents.iloc[i])

        print(f'Finished translating {subint} in {time.perf_counter() - start:.4f} secs')

    trans_text_df = pd.DataFrame(zip(trans_text, trans_subint), columns=['utterance', 'subintent'])

    # Exporting the translated utterances
    export_name = cmd_args.translate + '.csv'
    trans_text_df.to_csv(export_name, index=False)
    print(f'Total time elapsed: {time.perf_counter() - start:.4f} secs')
