import argparse

_TRANSLATE_HELP = 'Details (TO and FROM languages) for the translation to be done. Can be either of en_fr or en_es'
_DATA_PATH_HELP = 'Path to the input dataframe containing at least English utterances & subintent columns'
_SUBSET_HELP = 'Whether to translate only a specific subintent. Default is None. If None, complete dataframe will be ' \
               'translated. Mention the name of subintent otherwise.'


def init_cmd_args(args):
    parser = argparse.ArgumentParser()

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument('--data_path', type=str, required=True, help=_DATA_PATH_HELP)
    required_args.add_argument('--translate', type=str, required=True, help=_TRANSLATE_HELP)

    optional_args = parser.add_argument_group("optional arguments")
    optional_args.add_argument('--subset', type=str, required=False, default=None, help=_SUBSET_HELP)

    return parser.parse_args(args)

