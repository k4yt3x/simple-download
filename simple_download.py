#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Simple Download
Author: K4YT3X
Date of Creation: August 12, 2019
Last Modified: August 12, 2019

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt

(C) 2018-2019 K4YT3X

Version: 1.0.0
"""

# built-in imports
import pathlib
import re
import urllib

# third-party imports
from tqdm import tqdm
import requests


def download(url, save_as=None, save_path=None, chunk_size=4096):
    """ download file to local with requests library

    Arguments:
        url {string} -- download url
        save_as {string/pathlib.Path} -- output file (default: {None})
        save_path {string/pathlib.Path} -- folder to save downloaded file to (default: {None})

    Keyword Arguments:
        chunk_size {number} -- download stream chunk size (default: {4096})

    Returns:
        pathlib.Path -- full path of downloaded file
    """

    # create requests stream for steaming file
    stream = requests.get(url, stream=True, allow_redirects=True)

    # determine output file path
    # if exact output file name specified
    if save_as:
        output_file = pathlib.Path(save_as)

    # if output directory specified
    # or if no output is specified
    else:

        # get file name
        file_name = None
        if 'content-disposition' in stream.headers:
            disposition = stream.headers['content-disposition']
            try:
                file_name = re.findall("filename=(.+)", disposition)[0].strip('"')
            except IndexError:
                pass

        # if save_path is not specified, use current directory
        if save_path is None:
            save_path = pathlib.Path('.')
        else:
            save_path = pathlib.Path(save_path)

        # create target folder if it doesn't exist
        save_path.mkdir(parents=True, exist_ok=True)

        # if no file name could be determined
        # create file name from URL
        if file_name is None:
            output_file = save_path / stream.url.split('/')[-1]
        else:
            output_file = save_path / file_name

        # decode url encoding
        output_file = pathlib.Path(urllib.parse.unquote(str(output_file)))

    # get total size for progress bar if provided in headers
    total_size = 0
    if 'content-length' in stream.headers:
        total_size = int(stream.headers['content-length'])

    # print download information summary
    print(f'Downloading: {url}')
    print(f'Total size: {total_size}')
    print(f'Chunk size: {chunk_size}')
    print(f'Saving to: {output_file}')

    # write content into file
    with open(output_file, 'wb') as output:
        with tqdm(total=total_size, ascii=True) as progress_bar:
            for chunk in stream.iter_content(chunk_size=chunk_size):
                if chunk:
                    output.write(chunk)
                    progress_bar.update(len(chunk))

    # return the full path of saved file
    return output_file
