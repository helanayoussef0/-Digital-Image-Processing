import numpy as np
from numpy.testing import assert_allclose
import pytest
from pytest import approx
from skimage import data
from skimage.io import imsave
from skimage.util import img_as_float, img_as_ubyte

from assignment.colour_space import YCbCrColourSpace


def test_q1a_rgb_to_ycbcr_conversion():
    # The RGB to YCbCr transform is linear, giving a 1:1 mapping between the
    # two.  This test checks for that along with some pre-computed RGB/YCbCr
    # colour pairs.  It effectively samples the values from the transformation
    # matrix.
    converter = YCbCrColourSpace()

    red = np.zeros((1, 1, 3))
    red[0, 0, 0] = 1
    Y, cbcr = converter.to_ycbcr(red)
    assert Y == 0.299
    assert cbcr[0, 0, 0] == -0.1687
    assert cbcr[0, 0, 1] == 0.5

    green = np.zeros((1, 1, 3))
    green[0, 0, 1] = 1
    Y, cbcr = converter.to_ycbcr(green)
    assert Y == 0.587
    assert cbcr[0, 0, 0] == -0.3313
    assert cbcr[0, 0, 1] == -0.4187

    blue = np.zeros((1, 1, 3))
    blue[0, 0, 2] = 1
    Y, cbcr = converter.to_ycbcr(blue)
    assert Y == 0.114
    assert cbcr[0, 0, 0] == 0.5
    assert cbcr[0, 0, 1] == -0.0813


def test_q1b_ycbcr_to_rgb_conversion():
    # The YCbCr to RGB transform is linear, giving a 1:1 mapping between the
    # two.  This tests if the colour can be recovered from the YCbCr tuple,
    # which is slightly different from the above test.
    converter = YCbCrColourSpace()

    def format_values(Y, Cb, Cr):
        Yout = np.zeros((1, 1))
        Yout[0, 0] = Y
        cbcr = np.zeros((1, 1, 2))
        cbcr[0, 0, 0] = Cb
        cbcr[0, 0, 1] = Cr
        return Yout, cbcr

    # The 'approx' accounts for the imprecision arising from the number of
    # significant digits in the YCbCr formula.  A tolerance of 1/512 means that
    # the numbers are to within a precision of 9-bits.

    ycbcr_red = format_values(0.299, -0.1687, 0.5)
    rgb = converter.to_rgb(*ycbcr_red)
    assert rgb[0, 0, 0] == approx(1.0, abs=1/512)
    assert rgb[0, 0, 1] == approx(0.0, abs=1/512)
    assert rgb[0, 0, 2] == approx(0.0, abs=1/512)

    ycbcr_green = format_values(0.587, -0.3313, -0.4187)
    rgb = converter.to_rgb(*ycbcr_green)
    assert rgb[0, 0, 0] == approx(0.0, abs=1/512)
    assert rgb[0, 0, 1] == approx(1.0, abs=1/512)
    assert rgb[0, 0, 2] == approx(0.0, abs=1/512)

    ycbcr_blue = format_values(0.114, 0.5, -0.0813)
    rgb = converter.to_rgb(*ycbcr_blue)
    assert rgb[0, 0, 0] == approx(0.0, abs=1/512)
    assert rgb[0, 0, 1] == approx(0.0, abs=1/512)
    assert rgb[0, 0, 2] == approx(1.0, abs=1/512)


def test_q1c_invalid_sampling_throws_error():
    with pytest.raises(ValueError):
        YCbCrColourSpace(0.5)


def test_q1d_can_convert_image(tmp_path):
    # Applying an RGB to YCbCr to RGB conversion should result in the original
    # image, with the caveat that the number of significant digits in the
    # transform values produces some error.
    img = data.astronaut()
    imsave(tmp_path / 'original.png', img)

    converter = YCbCrColourSpace()
    y, cbcr = converter.to_ycbcr(img)
    recovered = converter.to_rgb(y, cbcr)

    tmp = np.zeros(cbcr.shape[:2] + (3,))
    tmp[:, :, 0] = cbcr[:, :, 0] + 0.5
    tmp[:, :, 1] = cbcr[:, :, 1] + 0.5
    imsave(tmp_path / 'luma.png', img_as_ubyte(y))
    imsave(tmp_path / 'chroma.png', img_as_ubyte(tmp))
    imsave(tmp_path / 'recovered.png', img_as_ubyte(recovered))

    assert_allclose(recovered, img_as_float(img), atol=1/512)


def test_q1e_can_resample_chroma():
    img = data.astronaut()

    converter = YCbCrColourSpace(2)
    y, cbcr = converter.to_ycbcr(img)

    assert y.shape == img.shape[:2]
    assert cbcr.shape[0] == y.shape[0] // 2
    assert cbcr.shape[1] == y.shape[0] // 2

    recovered = converter.to_rgb(y, cbcr)
    assert recovered.shape == img.shape


def test_q1f_converting_greyscale_image_throws_error():
    converter = YCbCrColourSpace()
    with pytest.raises(ValueError):
        img = np.zeros((10, 10))
        converter.to_ycbcr(img)


def test_q1f_invalid_ycbcr_format_throws_error():
    converter = YCbCrColourSpace()

    # luma isn't single-channel
    with pytest.raises(ValueError):
        Y = np.zeros((3, 3, 3))
        cbcr = np.zeros((3, 3, 2))
        converter.to_rgb(Y, cbcr)

    # chroma isn't 2-channel
    with pytest.raises(ValueError):
        Y = np.zeros((3, 3))
        cbcr = np.zeros((3, 3, 3))
        converter.to_rgb(Y, cbcr)
