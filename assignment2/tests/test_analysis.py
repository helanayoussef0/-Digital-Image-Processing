import numpy as np
from numpy.testing import assert_array_equal
import pytest

from assignment import analysis


def test_q1a_can_generate_histogram():
    # The following image will produce a completely flat histogram.
    img = np.reshape(np.arange(256), (16, 16)).astype(np.uint8)
    hist = analysis.histogram(img)
    assert_array_equal(hist, np.ones_like(hist))


def test_q1b_reject_invalid_datatype():
    float_image = np.ones((10, 10), dtype=float)
    with pytest.raises(TypeError):
        analysis.histogram(float_image)


def test_q1c_reject_colour_images():
    colour_image = np.ones((10, 10, 3), dtype=np.uint8)
    with pytest.raises(ValueError):
        analysis.histogram(colour_image)
