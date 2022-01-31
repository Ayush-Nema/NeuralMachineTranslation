import os
import json
import argparse
import logging
import logging.config as logging_config

LOGGER = logging.getLogger(__name__)

_TRANSLATE_HELP = 'Details (TO and FROM languages) for the translation to be done. Some valid examples are en-fr, en-es'
_INPUT_PATH_HELP = 'Path to the input data file or directory containing utterances'
_ISDIR_HELP = 'Whether the directory address is passed to input_path field. Mention the flag if directory is passed instead of filename'
_OUTPUT_PATH_HELP = 'The file path for the output file(s). The default path is `/data/output`.'
_LOG_CONFIG_FILE_HELP = "Path to the logger configuration"


def init_cmd_args(args):
    parser = argparse.ArgumentParser(description='A project on Neural Machine Translation using pretrained models')

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument('-d', '--input_path', type=str, required=True, help=_INPUT_PATH_HELP)
    required_args.add_argument('-t', '--translate', type=str, required=True, help=_TRANSLATE_HELP)

    optional_args = parser.add_argument_group("optional arguments")
    optional_args.add_argument('--isdir', action='store_true', help=_ISDIR_HELP)
    optional_args.add_argument("--logger_config", type=str, required=False, help=_LOG_CONFIG_FILE_HELP)
    optional_args.add_argument('-o', '--output_path', required=False, default='./data/output', help=_OUTPUT_PATH_HELP)

    # Sanity check for output directory
    check_directory('./data/output')

    return parser.parse_args(args)


def config_logger(log_config_fp):
    """
    Config the logging framework
    :param log_config_fp: The path to the logging framework's configuration file
    :type log_config_fp: str
    :return: Nothing
    :rtype: None
    :raises FileNotFoundError: If the file cannot be found at the given path
    :raises TypeError: If the log_config_fp is not a string
    """
    if not issubclass(type(log_config_fp), str):
        raise TypeError("Logging framework configuration file path has to be a string")

    if not os.path.exists(log_config_fp):
        raise FileNotFoundError("Cannot find the logging framework configuration file at the given path")

    with open(log_config_fp, "r") as log_config_file:
        log_conf = json.load(fp=log_config_file)

        logging_config.dictConfig(log_conf)

        LOGGER.info("Logging framework initialised!")


def check_directory(fp):
    if not os.path.isdir(fp):
        os.mkdir("./data/output", mode=0o666)
