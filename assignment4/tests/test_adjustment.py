import numpy as np
from numpy.testing import assert_array_equal

import pytest
from skimage import data
from skimage.io import imsave
from skimage.util import img_as_float, img_as_ubyte

from assignment import adjustment


def test_q3a_apply_saturation_adjustment(tmp_path):
    img = data.coffee()
    imsave(tmp_path / 'original.png', img)

    for i, amount in enumerate([-1, -0.5, 0, 0.5, 1]):
        adj = adjustment.adjust_saturation(img, amount)
        imsave(tmp_path / f'adjusted-{i+1}.png', img_as_ubyte(adj))


def test_q3b_adjusting_saturation_for_greyscale_image_throws_error():
    with pytest.raises(ValueError):
        adjustment.adjust_saturation(np.zeros((3, 3)), 0)


def test_q3c_invalid_adjustment_amount_throws_error():
    img = data.coffee()
    with pytest.raises(ValueError):
        adjustment.adjust_saturation(img, -5)

    with pytest.raises(ValueError):
        adjustment.adjust_saturation(img, 5)


def test_q4a_apply_hue_adjustment(tmp_path):
    img = data.rocket()
    imsave(tmp_path / 'original.png', img)

    # Adjust the hue in 45-degree increments.
    for amount in range(0, 361, 45):
        adj = adjustment.adjust_hue(img, amount)
        imsave(tmp_path / f'adjusted-{amount}.png', img_as_ubyte(adj))


def test_q4b_adjusting_hue_of_greyscale_image_throws_error():
    with pytest.raises(ValueError):
        adjustment.adjust_hue(np.zeros((10, 10)), 0)


def test_q5a_custom_rgb_to_grey():
    img = data.rocket()
    img = img_as_float(img)

    # Setting a weight to '1' and the rest to '0' is equivalent to selecting a
    # particular colour channel.
    assert_array_equal(adjustment.to_monochrome(img, 1, 0, 0), img[:, :, 0])
    assert_array_equal(adjustment.to_monochrome(img, 0, 1, 0), img[:, :, 1])
    assert_array_equal(adjustment.to_monochrome(img, 0, 0, 1), img[:, :, 2])


def test_q5b_making_greyscale_image_monochrome_throws_error():
    with pytest.raises(ValueError):
        adjustment.to_monochrome(np.ndarray((10, 10)), 1/3, 1/3, 1/3)


def test_q5c_negative_weights_throw_errors():
    img = data.rocket()
    with pytest.raises(ValueError):
        adjustment.to_monochrome(img, -1/3, 1/3, 1/3)

    with pytest.raises(ValueError):
        adjustment.to_monochrome(img, 1/3, -1/3, 1/3)

    with pytest.raises(ValueError):
        adjustment.to_monochrome(img, 1/3, 1/3, -1/3)
