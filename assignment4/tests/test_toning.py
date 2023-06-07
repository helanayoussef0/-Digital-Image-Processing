import pathlib

import pytest
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte

from assignment.toning import single_tone, split_tone


def test_q6a_perform_single_toning(tmp_path):
    img = imread(pathlib.Path() / 'samples' / 'rubiks-cube.jpg')
    out = single_tone(img, 45, 1, 0.5)  # tones with a yellow-ish colour
    imsave(tmp_path / 'single-tone.png', img_as_ubyte(out))


def test_q6b_perform_single_toning_with_greyscale(tmp_path):
    img = imread(pathlib.Path() / 'samples' / 'rubiks-cube.jpg', as_gray=True)
    imsave(tmp_path / 'grey.png', img_as_ubyte(img))
    out = single_tone(img, 45, 1, 1.0)
    imsave(tmp_path / 'single-tone.png', img_as_ubyte(out))


def test_q6c_error_thrown_with_invalid_hue():
    img = imread(pathlib.Path() / 'samples' / 'rubiks-cube.jpg')

    with pytest.raises(ValueError):
        single_tone(img, -10, 0.5)

    with pytest.raises(ValueError):
        single_tone(img, 400, 0.5)


def test_q6d_error_thrown_with_invalid_saturation():
    img = imread(pathlib.Path() / 'samples' / 'rubiks-cube.jpg')

    with pytest.raises(ValueError):
        single_tone(img, 0, -0.5)

    with pytest.raises(ValueError):
        single_tone(img, 0, 1.5)


def test_q6e_error_thrown_with_invalid_amount():
    img = imread(pathlib.Path() / 'samples' / 'rubiks-cube.jpg')

    with pytest.raises(ValueError):
        single_tone(img, 0, 0.5, -1.0)

    with pytest.raises(ValueError):
        single_tone(img, 0, 0.5, 2.0)


def test_q6f_perform_split_toning(tmp_path):
    img = imread(pathlib.Path() / 'samples' / 'rubiks-cube.jpg')

    highlights = (100/360, 10/100)  # light green colour
    shadows = (0/360, 62/100)       # red-ish colour

    out = split_tone(img, highlights, shadows)
    imsave(tmp_path / 'split-tone.png', img_as_ubyte(out))
