#! /usr/bin/env python3

from nbconvert import HTMLExporter
import argparse
import os
import sys
import logging
logger = logging.getLogger(__name__)

def readable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            'not an existing directory: {}'.format(path))
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(
            'not a readable directory: {}'.format(path))
    return path

def yield_ipynb(topdir):
    for dirpath, dirnames, filenames in os.walk(topdir, topdown=True):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if filename.endswith('.ipynb'):
                if os.path.isfile(filepath):
                    logging.debug("path matches: '{}'".format(filepath))
                    yield filepath
                else:
                    logging.error("file does not exist: '{}'".format(filepath))
            else:
                logging.debug("Skipping path '{}'".format(filepath))
                continue

def convert_single_ipynb(filepath):
    parent_dir, filename = os.path.split(filepath)
    root, ext = os.path.splitext(filename)
    # TODO: handle other formats
    target_filename = root + '.html'
    target_filepath = os.path.join(parent_dir, target_filename)
    logging.info("target_filepath = '{}'".format(target_filepath))
    html_exporter = HTMLExporter(template_name = 'classic')
    (html_txt, resources) = html_exporter.from_filename(filepath)
    with open(target_filepath, 'w') as fp:
        fp.write(html_txt)

def convert_recursive(topdir, no_action=False):
    for path in yield_ipynb(topdir):
        if not no_action:
            convert_single_ipynb(path)
        else:
            print(path)

def main():
    parser = argparse.ArgumentParser(
        description='Recursively convert .ipynb files to HTML.')
    # Temporary, these will be directories later.
    parser.add_argument(
        'topdir',
        type=readable_directory,
        help='directory to look under',
    )
    parser.add_argument(
        '-n',
        '--no-act',
        action='store_true',
        help="Don't actually convert anything.",
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

    convert_recursive(args.topdir, no_action=args.no_act)

if __name__ == '__main__':
    main()
