#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
import argparse
import os
import re

from PIL import Image

def check_args():
    '''
    Image.NEAREST -> 0
    Image.ANTIALIAS -> 1
    Image.BILINEAR -> 2
    Image.BICUBIC -> 3
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', help='original image directory')
    parser.add_argument('-o', '--output', help='resized output directory')
    parser.add_argument('-s', '--size', help='thumbnail size', type=int, default=640)
    parser.add_argument('-q', '--quality', help='resize quality (0-100)', type=int,
                        default=80)
    parser.add_argument('-a', '--algorithm', help='resize algorithm (0-3)', type=int,
                        default=Image.ANTIALIAS)

    return parser.parse_args()

def main():
    pattern = '^.+(\d{6}).+$'
    rc = re.compile(pattern)
    args = check_args()
    algorithm = Image.ANTIALIAS
    os.makedirs(args.output, exist_ok=True)
    for x in os.listdir(args.input):
        m = rc.match(x)
        if m:
            g = m.groups()
            try:
                im = Image.open(os.path.join(args.input, x))
                im.thumbnail((args.size, args.size), algorithm)
                im.save(os.path.join(args.output, f'{g[0]}.jpg'), quality=args.quality)
            except Exception as e:
                print (e)
    if not len(os.listdir(args.output)):
        os.rmdir(args.output)

if __name__ == "__main__":
    main()
##### rename.py ends here
