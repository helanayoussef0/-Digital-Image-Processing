import numpy as np
from skimage.color import hsv2rgb, rgb2hsv
from skimage.util import img_as_float


def single_tone(img, hue, saturation, amount=1.0):
    '''Apply a colour tone to an image.

    The toning process is the same for both greyscale and colour image.  Colour
    images are simply converted into HSV.  A greyscale image is "converted" to
    colour by replicating it three times before converting it into HSV.

    Parameters
    ----------
    img : numpy.ndarray
        a colour or greyscale input image; the data type will be converted to
        float if it is not already
    hue : float
        the value of the tone's hue; must be an angle on [0, 360]
    saturation : float
        the tone's saturation; must be on [0, 1]
    amount : float, optional
        a value between 0 and 1 on how much of the tone to apply to the original
        image; the default is 1.0, or completely replace all colour

    Returns
    -------
    numpy.ndarray
        the colour-toned image

    Raises
    ------
    ValueError
        if any of the input values are invalid
    '''
    raise NotImplementedError('Implement this function/method.')


def split_tone(img, highlight, shadow):
    '''Apply split toning to an image.

    Parameters
    ----------
    img : numpy.ndarray
        input RGB image
    highlight : (hue, saturation)
        the highlight tone
    shadow : (hue, saturation)
        the shadow tone

    Returns
    -------
    numpy.ndarray
        the split-toned image
    '''
    raise NotImplementedError('Implement this function/method.')
