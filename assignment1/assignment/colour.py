import numpy as np


def rgb2grey(image):
    '''Convert a RGB colour image into a greyscale image.

    The image is converted into RGB by taking a weighted sum of the three colour
    channels.  I.e.,

    .. math::

        I(x,y) = 0.299 R(x,y) + 0.587 G(x,y) + 0.114 B(x,y).

    The image should be converted to floating point prior to the calculation so
    that it's on [0, 1].  After generating the greyscale image, it should be
    converted back to 8bpc.

    Parameters
    ----------
    image : numpy.ndarray
        a 3-channel, RGB image

    Returns
    -------
    numpy.ndarray
        a single channel, monochome image derived from the original

    Raises
    ------
    ValueError
        if the image is already greyscale or if the input image isn't 8bpc
    '''
    raise NotImplementedError('Implement this function/method.')


def grey2rgb(image):
    '''Pseudo-convert a greyscale image into an RGB image.

    This will make an greyscale image appear to be RGB by duplicating the
    intensity channel three times.

    Parameters
    ----------
    image : numpy.ndarray
        a greyscale image

    Returns
    -------
    numpy.ndarray
        a three-channel, RGB image

    Raises
    ------
    ValueError
        if the input image is already RGB or if the image isn't 8bpc
    '''
    raise NotImplementedError('Implement this function/method.')
