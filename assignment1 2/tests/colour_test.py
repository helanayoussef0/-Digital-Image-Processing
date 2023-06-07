import pathlib

import numpy as np
from numpy.testing import assert_array_equal
import pytest

from assignment.colour import rgb2grey, grey2rgb
from assignment.io import imread


def test_q3a_convert_rgb_to_greyscale():
    colour_file = pathlib.Path() / 'samples' / 'rocket.ppm'
    grey_file = pathlib.Path() / 'samples' / 'rocket-greyscale.pgm'

    image = imread(str(colour_file))

    greyscale = rgb2grey(image)
    expected = imread(str(grey_file))

    assert greyscale.dtype == np.uint8
    assert_array_equal(greyscale, expected)


def test_q3b_rgb2grey_handles_invalid_inputs():
    float_rgb = np.zeros((10, 10, 3), dtype=np.float)
    uint8_greyscale = np.zeros((10, 10), dtype=np.uint8)

    with pytest.raises(ValueError):
        rgb2grey(float_rgb)

    with pytest.raises(ValueError):
        rgb2grey(uint8_greyscale)


def test_q4a_convert_grey_to_pseudo_colour():
    grey_file = pathlib.Path() / 'samples' / 'rocket-greyscale.pgm'
    image = imread(str(grey_file))

    rgb = grey2rgb(image)
    assert rgb.dtype == np.uint8
    assert rgb.ndim == 3
    assert rgb.shape[2] == 3

    for i in range(3):
        assert_array_equal(rgb[:, :, i], image)


def test_q4b_grey2rgb_handles_invalid_inputs():
    uint8_rgb = np.zeros((10, 10, 3), dtype=np.uint8)
    float_greyscale = np.zeros((10, 10), dtype=np.float)

    with pytest.raises(ValueError):
        grey2rgb(uint8_rgb)

    with pytest.raises(ValueError):
        grey2rgb(float_greyscale)
