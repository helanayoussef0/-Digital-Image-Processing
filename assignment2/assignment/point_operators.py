import numpy as np


def apply_lut(img, lut):
    '''Apply a look-up table to an image.

    The look-up table can be be used to quickly adjust the intensities within an
    image.  For colour images, the same LUT can be applied equally to each
    colour channel.

    Parameters
    ----------
    img : numpy.ndarray
        a ``H x W`` greyscale or ``H x W x C`` colour 8bpc image
    lut : numpy.ndarray
        a 256-element, 8-bit array

    Returns
    -------
    numpy.ndarray
        a new ``H x W`` or ``H x W x C`` image derived from applying the LUT

    Raises
    ------
    ValueError
        if the LUT is not 256-elements long
    TypeError
        if either the LUT or images are not 8bpc
    '''
    raise NotImplementedError('Implement this function/method.')


def adjust_brightness(offset):
    '''Generate a LUT to adjust the image brightness.

    Parameters
    ----------
    offset : int
        the amount to offset brightness values by; this may be negative or
        positive

    Returns
    -------
    numpy.ndarray
        a 256-element LUT that can be provided to ``apply_lut()``
    '''
    raise NotImplementedError('Implement this function/method.')


def adjust_contrast(scale, hist):
    '''Generate a LUT to adjust contrast without affecting brightness.

    Parameters
    ----------
    scale : float
        the value used to adjust the image contrast; a value greater than 1 will
        increase constrast while a value less than 1 will reduce it
    hist : numpy.ndarray
        a 256-element array containing the image histogram, which is used to
        calculate the image brightness

    Returns
    -------
    numpy.ndarray
        a 256-element LUT that can be provided to ``apply_lut()``

    Raises
    ------
    ValueError
        if the histogram is not 256-elements or if the scale is less than zero
    '''
    raise NotImplementedError('Implement this function/method.')


def adjust_exposure(gamma):
    '''Generate a LUT that applies a power-law transform to an image.

    Parameters
    ----------
    gamma : float
        the exponent in the power-law transform; must be a positive value

    Returns
    -------
    numpy.ndarray
        a 256-element LUT that can be provided to ``apply_lut()``

    Raises
    ------
    ValueError
        if ``gamma`` is negative
    '''
    raise NotImplementedError('Implement this function/method.')


def log_transform():
    '''Generate a LUT that applies a log-transform to an image.

    Returns
    -------
    numpy.ndarray
        a 256-element LUT that can be provided to ``apply_lut()``
    '''
    raise NotImplementedError('Implement this function/method.')
