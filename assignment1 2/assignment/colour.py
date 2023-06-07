import numpy as np


def rgb2grey(image):
    """Convert a RGB colour image into a greyscale image.

    The image is converted into greyscale by taking a weighted sum of the three color
    channels. The conversion equation is:
        I'(x, y) = 0.299 * R(x, y) + 0.587 * G(x, y) + 0.114 * B(x, y)

    The image should be converted to floating-point prior to the calculation so
    that it's in the range [0, 1]. After generating the greyscale image, it should be
    converted back to 8-bit per channel (8bpc).

    Parameters:
    image (numpy.ndarray): a 3-channel, RGB image

    Returns:
    numpy.ndarray: a single channel, monochrome image derived from the original

    Raises:
    ValueError: if the image is already greyscale or if the input image isn't 8bpc
    """
    if len(image.shape) == 2:
        raise ValueError("The image is already greyscale")
    if image.shape[2] != 3:
        raise ValueError("The input image isn't 8bpc")
    grey = np.dot(image[..., :3], [0.299, 0.587, 0.114])
    return grey.astype(np.uint8)


def grey2rgb(image):
    """Pseudo-convert a greyscale image into an RGB image.

    This function makes a greyscale image appear to be RGB by duplicating the
    intensity channel three times.

    Parameters:
    image (numpy.ndarray): a greyscale image

    Returns:
    numpy.ndarray: a three-channel, RGB image

    Raises:
    ValueError: if the input image is already RGB or if the image isn't 8bpc
    """
    if len(image.shape) == 3:
        raise ValueError("The input image is already RGB")
    return np.repeat(image[..., np.newaxis], 3, axis=-1).astype(np.uint8)
