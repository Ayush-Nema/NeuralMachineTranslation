import sys
import time
import pandas as pd
import concurrent.futures as multiprocess
from transformers import MarianTokenizer, AutoModelForSeq2SeqLM
from utilities.utility import init_cmd_args

# Parsing the command line arguments
cmd_args = init_cmd_args(sys.argv[1:])

# Reading the dataframe
data = pd.read_csv(cmd_args.data_path)

# Simple data analysis (finding the count of unique subintent values)
df = data.groupby('subintent')['utterance'].nunique()

# Sub-setting the data based on subintent (for test purposes)
if cmd_args.subset is not None:
    data = data[data['subintent'] == cmd_args.subset]

en_utts = data.utterance
subintents = data.subintent

# Loading the pre-trained model
if cmd_args.translate == 'en_fr':
    mname = 'Helsinki-NLP/opus-mt-en-fr'
else:
    mname = 'Helsinki-NLP/opus-mt-en-es'

tokenizer = MarianTokenizer.from_pretrained(mname)
model = AutoModelForSeq2SeqLM.from_pretrained(mname)


def translator(text):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(input_ids)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded


if __name__ == '__main__':
    start = time.perf_counter()

    with multiprocess.ProcessPoolExecutor(max_workers=7) as executor:
        trans_text = executor.map(translator, en_utts.to_list())

        op_list = []
        for non_en_utt in trans_text:
            op_list.append(non_en_utt)

    trans_text_df = pd.DataFrame(zip(op_list, subintents.to_list()), columns=['utterance', 'subintent'])

    print(f'Finished translation in {time.perf_counter() - start:.4f} secs')

    export_name = cmd_args.translate + '.csv'
    trans_text_df.to_csv(export_name, index=False)
