#! /usr/bin/env python3

from nbconvert import HTMLExporter
import argparse
import os
import sys
import logging
logger = logging.getLogger(__name__)

def readable_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(
            'not an existing file: {}'.format(path))
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(
            'not a readable file: {}'.format(path))
    return path

def main():
    parser = argparse.ArgumentParser(
        description='Recursively convert .ipynb files to HTML.')
    # Temporary, these will be directories later.
    parser.add_argument(
        'input', type=readable_file)
    parser.add_argument(
        'output',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='More verbose logging',
        dest="loglevel",
        default=logging.WARNING,
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Enable debugging logs',
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    logger.setLevel(args.loglevel)

    html_exporter = HTMLExporter(template_name = 'classic')
    (html, resources) = html_exporter.from_filename(args.input)
    with open(args.output, 'w') as fp:
        fp.write(html)

if __name__ == '__main__':
    main()
