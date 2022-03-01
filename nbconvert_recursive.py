#! /usr/bin/env python3

import nbformat
from nbconvert import HTMLExporter
import sys

filepath = sys.argv[1]

#notebook = nbformat.from_filename(filepath)
html_exporter = HTMLExporter(template_name = 'classic')
(html, resources) = html_exporter.from_filename(filepath)
#import ipdb
#ipdb.set_trace()
with open('out.html', 'w') as fp:
    fp.write(html)
