import pathlib

import matplotlib.pyplot as plt
import numpy as np
from numpy.testing import assert_array_equal
import pytest
import skimage.data

from skimage.color import rgb2gray
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte

from assignment import analysis, point_operators


class _Stats:
    def __init__(self):
        self.brightness = 0
        self.contrast = 0


def _plot_transfer_function(lut, folder):
    '''Plot the LUT to an image.

    Parameters
    ----------
    lut : numpy.ndarray
        look-up table
    folder : path-like object
        path to where the plot is saved
    '''
    plt.figure()
    plt.plot(lut)
    plt.xlabel('r')
    plt.ylabel('T(r)')
    plt.title('Transfer Function')
    plt.savefig(folder / 'transfer-function.png')


def _compare_stats_after_applying_lut(img, lut, folder):
    '''Compare statistics after applying the LUT to an image.

    Both the original and processed image will be saved to the specified folder.

    Parameters
    ----------
    img : numpy.ndarray
        input image
    lut : numpy.ndarray
        look-up table
    folder : path-like object
        path to folder where the original image and adjusted image can be saved

    Returns
    -------
    original_stats : ``(brightness, contrast)``
        original image statistics
    processed_stats : ``(brightness, contrast)``
        post-application image statistics
    '''
    img = rgb2gray(img)
    img = img_as_ubyte(img)

    original_stats = _Stats()
    original_stats.brightness = analysis.estimate_brightness(img)
    original_stats.contrast = analysis.estimate_contrast(img)

    processed = point_operators.apply_lut(img, lut)

    processed_stats = _Stats()
    processed_stats.brightness = analysis.estimate_brightness(processed)
    processed_stats.contrast = analysis.estimate_contrast(processed)

    imsave(folder / 'original.png', img)
    imsave(folder / 'processed.png', processed)

    return original_stats, processed_stats


def test_q2a_apply_lut_to_valid_greyscale_image():
    # Use an image that contains all of the 8-bit values and use a LUT to
    # perform a simple 1/2 scaling.  The combination of the image's contents and
    # the LUT's size means that the output image will be identical to the LUT
    # after reshaping.
    img = np.reshape(np.arange(256, dtype=np.uint8), (16, 16))
    lut = np.arange(256, dtype=np.uint8) // 2

    expected = np.reshape(lut, (16, 16))

    out = point_operators.apply_lut(img, lut)
    assert_array_equal(out, expected)


def test_q2b_apply_lut_to_valid_colour_image():
    # Same logic as previous test, just with a colour image.
    plane = np.reshape(np.arange(256, dtype=np.uint8), (16, 16))
    img = np.dstack((plane, plane, plane))
    lut = np.arange(256, dtype=np.uint8) // 2

    plane = np.reshape(lut, (16, 16))
    expected = np.dstack((plane, plane, plane))

    out = point_operators.apply_lut(img, lut)
    assert_array_equal(out, expected)


def test_q2c_invalid_image_type_raises_error():
    lut = np.arange(256, dtype=np.uint8)
    img = np.ones((10, 10), dtype=float)
    with pytest.raises(TypeError):
        point_operators.apply_lut(img, lut)


def test_q2d_invalid_lut_type_raises_error():
    lut = np.arange(256)
    img = np.ones((10, 10), dtype=np.uint8)
    with pytest.raises(TypeError):
        point_operators.apply_lut(img, lut)


def test_q2e_invalid_lut_length_raises_error():
    lut = np.arange(10, dtype=np.uint8)
    img = np.ones((10, 10), dtype=np.uint8)
    with pytest.raises(ValueError):
        point_operators.apply_lut(img, lut)


def test_q3a_brightness_adjustment(tmp_path):
    # This is the Figure 4 from the original assignment.  The brightness
    # adjustment should change the brightness without affecting contrast.
    img = skimage.data.rocket()

    lut = point_operators.adjust_brightness(50)
    _plot_transfer_function(lut, tmp_path)
    original_stats, processed_stats = _compare_stats_after_applying_lut(img, lut, tmp_path)

    assert processed_stats.brightness == (original_stats.brightness + 50)
    assert processed_stats.contrast == original_stats.contrast


def test_q3b_contrast_adjustment(tmp_path):
    # This is Figure 6 from the assignment document.  The contrast should be
    # 1.5 times the original image.  The brightness should be unchanged (if
    # working in floating point the value may change very slightly due to the
    # quantization).
    img = skimage.data.rocket()

    hist = analysis.histogram(img_as_ubyte(rgb2gray(img)))
    lut = point_operators.adjust_contrast(1.5, hist)
    _plot_transfer_function(lut, tmp_path)
    original_stats, processed_stats = _compare_stats_after_applying_lut(img, lut, tmp_path)

    assert processed_stats.brightness == original_stats.brightness
    assert processed_stats.contrast == 1.5*original_stats.contrast


def test_q3c_exposure_adjustment(tmp_path):
    img = skimage.data.coffee()

    lut = point_operators.adjust_exposure(2.2)
    out = point_operators.apply_lut(img, lut)

    _plot_transfer_function(lut, tmp_path)
    imsave(tmp_path / 'original.png', img)
    imsave(tmp_path / 'processed.png', out)

    # Compare against a reference image.
    ref = imread(pathlib.Path() / 'samples' / 'reference' / 'exposure.png')
    assert_array_equal(out, ref)


def test_q3d_log_transform(tmp_path):
    img = skimage.data.hubble_deep_field()
    img = img_as_ubyte(rgb2gray(img))

    lut = point_operators.log_transform()
    out = point_operators.apply_lut(img, lut)

    _plot_transfer_function(lut, tmp_path)
    imsave(tmp_path / 'original.png', img)
    imsave(tmp_path / 'processed.png', out)

    # Compare against a reference image.
    ref = imread(pathlib.Path() / 'samples' / 'reference' / 'log-transform.png')
    assert_array_equal(out, ref)
