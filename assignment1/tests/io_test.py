import pathlib

import numpy as np
from numpy.testing import assert_array_equal
import pytest

from assignment.io import imread, imwrite


def test_q1a_read_greyscale_image():
    expected = np.array([
        [255, 0,   255, 255],
        [0,   255, 255, 255],
        [0,   255, 255, 0],
        [255, 0,   0,   255]
    ], dtype=np.uint8)

    filename = pathlib.Path() / 'samples' / 'greyscale.pgm'
    image = imread(filename.absolute())
    assert_array_equal(expected, image)


def test_q1b_read_colour_image():
    expected = np.array([
       [[255,   0,   0],
        [0,   0,   0],
        [255, 255, 255],
        [255, 255, 255]],

       [[0,   0,    0],
        [0,   255,  0],
        [0,   0,    255],
        [255, 255,  255]],

       [[0,   0,   0],
        [255, 0,   0],
        [0,   255, 255],
        [0,   0,   0]],

       [[255, 255, 0],
        [0,   0,   0],
        [0,   0,   0],
        [255, 0,   255]]
    ], dtype=np.uint8)

    filename = pathlib.Path() / 'samples' / 'colour.ppm'
    image = imread(filename.absolute())
    assert_array_equal(expected, image)


def test_q1c_unsupported_type_raises_exception():
    filename = pathlib.Path() / 'samples' / 'colour-binary.pbm'
    with pytest.raises(ValueError):
        imread(filename.absolute())


def test_q2a_write_greyscale_image(tmp_path):
    image = np.array([
        [255, 0,   255, 255],
        [0,   255, 255, 255],
        [0,   255, 255, 0],
        [255, 0,   0,   255]
    ], dtype=np.uint8)

    # write out the image file
    outfile = tmp_path / 'greyscale.pgm'
    imwrite(str(outfile), image)
    with outfile.open('rt') as f:
        generated = f.read().split()

    # compare it to the original
    pgmfile = pathlib.Path() / 'samples' / 'greyscale.pgm'
    with pgmfile.open('rt') as f:
        expected = f.read().split()

    assert generated == expected


def test_q2b_write_colour_image(tmp_path):
    image = np.array([
       [[255,   0,   0],
        [0,   0,   0],
        [255, 255, 255],
        [255, 255, 255]],

       [[0,   0,    0],
        [0,   255,  0],
        [0,   0,    255],
        [255, 255,  255]],

       [[0,   0,   0],
        [255, 0,   0],
        [0,   255, 255],
        [0,   0,   0]],

       [[255, 255, 0],
        [0,   0,   0],
        [0,   0,   0],
        [255, 0,   255]]
    ], dtype=np.uint8)

    # write out the image file
    outfile = tmp_path / 'colour.ppm'
    imwrite(str(outfile), image)
    with outfile.open('rt') as f:
        generated = f.read().split()

    # compare it to the original
    pgmfile = pathlib.Path() / 'samples' / 'colour.ppm'
    with pgmfile.open('rt') as f:
        expected = f.read().split()

    assert generated == expected
