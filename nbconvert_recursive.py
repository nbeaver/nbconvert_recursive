#! /usr/bin/env python3

from nbconvert import HTMLExporter
import sys

def main():
    filepath = sys.argv[1]
    html_exporter = HTMLExporter(template_name = 'classic')
    (html, resources) = html_exporter.from_filename(filepath)
    with open('out.html', 'w') as fp:
        fp.write(html)

if __name__ == '__main__':
    main()
