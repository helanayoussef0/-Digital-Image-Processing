import numpy as np


def histogram(img):
    '''Compute the histogram of an image.

    This function can only support processing 8bpc images, greyscale or colour.
    Colour images will produce three histograms (one per colour channel).

    Parameters
    ----------
    img : numpy.ndarray
        a ``H x W`` greyscale image

    Returns
    -------
    numpy.ndarray
        a 256-element, linear array containing the computed histogram

    Raises
    ------
    ValueError
        if the image isn't greyscale
    TypeError
        if the image isn't the ``numpy.uint8`` data type
    '''
    raise NotImplementedError('Implement this function/method.')


def estimate_brightness(img):
    '''Estimate the average image brightness.

    Parameters
    ----------
    img : numpy.ndarray
        a ``H x W`` greyscale image

    Returns
    -------
    int
        the average value of all image intensities, rounded to the nearest whole
        value

    Raises
    ------
    ValueError
        if the image is colour
    TypeError
        if the image isn't 8bpc
    '''
    if img.dtype != np.uint8:
        raise TypeError('Can only work on 8-bit images.')
    if img.ndim != 2:
        raise ValueError('Convert colour image to greyscale before processing.')

    return int(img.mean())


def estimate_contrast(img, percentile=0.95, provide_limits=False):
    '''Estimate the amount of contrast in the image.

    Parameters
    ----------
    img : numpy.ndarray
        a ``H x W`` greyscale image
    percentile : float, optional
        the percentile used to define the centre of mass, by default 0.95
    provide_limits : bool, optional
        if provided, then the limits are returned instead of the difference

    Returns
    -------
    contrast : int
        the estimated image contrast
    limits : ``(I_min, I_max)``
        a tuple containing the minimum/maximum contrast limits; only returned if
        ``provided_limits`` is ``True``
    '''
    if percentile <= 0.5:
        raise ValueError('Percentile must be larger than 0.5.')

    cdf = histogram(img).cumsum()
    cdf = cdf.astype(float) / cdf[-1]

    Imax = np.argwhere(cdf < percentile)[-1].squeeze()
    Imin = np.argwhere(cdf < 1 - percentile)[-1].squeeze()

    if provide_limits:
        return Imin, Imax
    else:
        return Imax - Imin
