#!/usr/bin/env python
# Copyright (c) 2015, NVIDIA CORPORATION.  All rights reserved.

"""
Classify an image using a model archive file
"""

import argparse
import os
import time
import zipfile
import tarfile
import tempfile

from example import classify

def unzip_archive(archive):
    """
    Unzips an archive into a temporary directory
    Returns a link to that directory

    Arguments:
    archive -- the path to an archive file
    """
    tmpdir = os.path.join(tempfile.gettempdir(),
            os.path.basename(archive))
    assert tmpdir != archive # That wouldn't work out

    if os.path.exists(tmpdir):
        # files are already extracted
        pass
    else:
        if tarfile.is_tarfile(archive):
            print 'Extracting tarfile ...'
            with tarfile.open(archive) as tf:
                tf.extractall(path=tmpdir)
        elif zipfile.is_zipfile(archive):
            print 'Extracting zipfile ...'
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(path=tmpdir)
        else:
            raise ValueError('Unknown file type for %s' % os.path.basename(archive))
    return tmpdir


def classify_with_archive(archive, image_files, use_gpu=True):
    """
    """
    tmpdir = unzip_archive(archive)
    caffemodel = None
    deploy_file = None
    mean_file = None
    labels_file = None
    for filename in os.listdir(tmpdir):
        full_path = os.path.join(tmpdir, filename)
        if filename.endswith('.caffemodel'):
            caffemodel = full_path
        elif filename == 'deploy.prototxt':
            deploy_file = full_path
        elif filename.endswith('.binaryproto'):
            mean_file = full_path
        elif filename == 'labels.txt':
            labels_file = full_path
        else:
            print 'Unknown file:', filename

    assert caffemodel is not None, 'Caffe model file not found'
    assert deploy_file is not None, 'Deploy file not found'

    classifications = classify(caffemodel, deploy_file, image_files,
            mean_file=mean_file, labels_file=labels_file, use_gpu=use_gpu)
    return classifications

if __name__ == '__main__':
    script_start_time = time.time()

    parser = argparse.ArgumentParser(description='Classification example using an archive - DIGITS')

    ### Positional arguments

    parser.add_argument('archive',  help='Path to a DIGITS model archive')
    parser.add_argument('image',    help='Path to an image')

    ### Optional arguments

    parser.add_argument('--nogpu',
            action='store_true',
            help="Don't use the GPU")

    args = vars(parser.parse_args())

    image_files = [args['image']]

    classify_with_archive(args['archive'], image_files, not args['nogpu'])

    print 'Script took %s seconds.' % (time.time() - script_start_time,)
