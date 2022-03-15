#! /usr/bin/env python3

from nbconvert import HTMLExporter
import argparse
import os
import sys
import logging
logger = logging.getLogger(__name__)

default_skip_dirs = [
    '.ipynb_checkpoints',
    '__pycache__',
    '.DS_Store',
    '.git',
    '.hg',
    '.svn',
    '.bzr',
    '_darcs',
]

def readable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            'not an existing directory: {}'.format(path))
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(
            'not a readable directory: {}'.format(path))
    return path

def yield_ipynb(topdir, skip_dirs=default_skip_dirs):
    logging.debug("topdir = '{}'".format(topdir))
    logging.debug("skip_dirs = '{}'".format(skip_dirs))
    for dirpath, dirnames, filenames in os.walk(topdir, topdown=True):
        logging.debug("dirpath = '{}'".format(dirpath))
        logging.debug("dirnames = '{}'".format(dirnames))
        logging.debug("filenames = '{}'".format(filenames))
        # Filter out skip_dirs.
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        logging.debug("dirnames = '{}'".format(dirnames))
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

def convert_single_ipynb(ipynb_filepath):
    logging.info("ipynb_filepath = '{}'".format(ipynb_filepath))
    parent_dir, filename = os.path.split(ipynb_filepath)
    root, ext = os.path.splitext(filename)
    # TODO: handle other formats
    target_filename = root + '.html'
    target_filepath = os.path.join(parent_dir, target_filename)
    logging.info("target_filepath = '{}'".format(target_filepath))
    html_exporter = HTMLExporter(template_name = 'classic')
    (html_txt, resources) = html_exporter.from_filename(ipynb_filepath)
    with open(target_filepath, 'w') as fp:
        fp.write(html_txt)

def convert_recursive(topdir, no_action=False, skip_dirs=default_skip_dirs):
    for path in yield_ipynb(topdir, skip_dirs=skip_dirs):
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
        '--skip-dirs',
        nargs='+',
        default=default_skip_dirs,
        help="Directories to skip, default = {}".format(default_skip_dirs),
    )
    parser.add_argument(
        '--extra-skip-dirs',
        nargs='+',
        default=None,
        help="Additional directories to skip.",
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

    if args.extra_skip_dirs is not None:
        all_skip_dirs = args.skip_dirs + args.extra_skip_dirs
    else:
        all_skip_dirs = args.skip_dirs

    convert_recursive(
        args.topdir,
        no_action=args.no_act,
        skip_dirs=all_skip_dirs,
    )

if __name__ == '__main__':
    main()
