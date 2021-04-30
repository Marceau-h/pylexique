# -*- coding: utf-8 -*-

"""Console CLI script for pylexique."""
import sys
import click
import json
import joblib
import logging
from pylexique import Lexique383, LexItem
from pprint import pprint
from collections import defaultdict


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument('words', nargs=-1)
@click.option('-o', '--output',
              default=None,
              help=("Path of the filename for storing the lexical entries"),
              type=click.STRING)
def main(words, output):
    """Pylexique is a Python wrapper around Lexique83.
    It allows to extract lexical information from more than 140 000 French words in an Object Oriented way.


    * Free software: MIT license
    * Documentation: https://pylexique.readthedocs.io.
    """
    logger = logging.getLogger(__name__)

    # create console handler and set level to debug
    console_handler = logging.StreamHandler(sys.stdout)
    error_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)

    LEXIQUE = Lexique383()
    results = defaultdict(list)
    for word in words:
        results[word].append(LEXIQUE.lexique[word])

        for i, element in enumerate(results[word]):
            if isinstance(element, LexItem):
                results[word][i] = element.to_dict()
                continue
            for index, item in enumerate(element):
                results[word][i][index] = item.to_dict()
    if output:
        with open(output, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=4)
            print('The Lexical Items have been successfully saved to {0} by pylexique.cli.main.'.format(output))
    else:
        if isinstance(words, tuple):
            for word in words:
                if isinstance(results[word], list):
                    for elmt in results[word]:
                        pprint(elmt.to_dict())
                        print('\n\n')
                else:
                    pprint(results[word])
                    print('\n\n')
    return


if __name__ == "__main__":
    main()  # pragma: no cover
