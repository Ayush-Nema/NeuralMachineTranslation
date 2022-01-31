import os
import sys
import time
import glob
import logging
import pandas as pd
from pathlib import Path
from functools import partial
from transformers import MarianTokenizer, AutoModelForSeq2SeqLM
from utilities.utils import init_cmd_args, config_logger
from source.translator import translate_text

__author__ = "ayush@gyandata.com"

# $ python3 main.py -d ./data/qrg_smoke_new.csv -t en-ro -o ./data/output/romanian-ro
# $ python3 main.py --isdir  -d ./data/data_copy/ -t en-sk -o ./data/output/slovak-sk

LOGGER = logging.getLogger(__name__)

_DEFAULT_LEVEL = "INFO"
_DEFAULT_FORMAT = "[%(asctime)s] - [%(levelname)s] - [%(name)s] : %(message)s"

# Parsing the command line arguments
cmd_args = init_cmd_args(sys.argv[1:])

# Check whether the logging file is supplied or not
if cmd_args.logger_config:
    config_logger(log_config_fp=cmd_args.logger_config)
else:
    logging.basicConfig(level=_DEFAULT_LEVEL, format=_DEFAULT_FORMAT)

# Retrieving the model name
model_name = f'Helsinki-NLP/opus-mt-{cmd_args.translate}'

# Initialising the pre-trained model
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Generate a partial function so as keep only one variable field
translate_func = partial(translate_text, tokenizer=tokenizer, model=model)


def _base_module(file_path):
    start_time = time.perf_counter()
    # Reading data and performing translation
    df = pd.read_csv(file_path)
    LOGGER.info(f'Initiating translation for {os.path.basename(file_path)} --> length={df.__len__()}')
    trans_txt = df.utterance.apply(lambda x: translate_func(x))
    df['translated_text'] = trans_txt

    # Exporting the translated utterances
    export_fname = f"{Path(file_path).stem}_{cmd_args.translate}.csv"
    df.to_csv(os.path.join(cmd_args.output_path, export_fname), index=False)

    # Curating the information
    total_time = time.perf_counter() - start_time
    LOGGER.info(f"{os.path.basename(file_path)} translated in {total_time:.3f} sec")
    LOGGER.info(f"Approximate throughput for {os.path.basename(file_path)} ≅ {total_time / df.shape[0]:0.3f}/sec")


if cmd_args.isdir:
    # If directory path is provided
    input_path = f'{cmd_args.input_path}/*.csv'
    for idx, val in enumerate(glob.glob(input_path)):
        _base_module(file_path=val)
        LOGGER.info(f"-------------- {idx + 1}/{len(os.listdir(cmd_args.input_path))} "
                    f"({(idx + 1)/(len(os.listdir(cmd_args.input_path)))*100:.2f}%) completed --------------")
else:
    # If file path is provided
    _base_module(file_path=cmd_args.input_path)
