import argparse


def command_line_with_default_values(default_val_dict):
    """
    This file is to take values from the command line, while preserving default values to run the file script from pycharm
    with hardcoded arguments.

    Default val dict is of the form
        {"var_name": value}
    :param default_val_dict:
    :return: Takes command line arguments and modifies the default val dict to contain those arguments.
    """

    for default_val_name in default_val_dict.keys():
        parser = argparse.ArgumentParser(description='Brain Amp fix.')
        parser.add_argument('--%s' % default_val_name, dest=default_val_dict[default_val_name], nargs='?', type=type(default_val_dict[default_val_name]),
                            default=default_val_dict[default_val_name])
    return default_val_dict
