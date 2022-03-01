#! /usr/bin/env python3

from nbconvert import HTMLExporter
import sys

filepath = sys.argv[1]

#notebook = nbformat.from_filename(filepath)
html_exporter = HTMLExporter(template_name = 'classic')
(html, resources) = html_exporter.from_filename(filepath)
with open('out.html', 'w') as fp:
    fp.write(html)
