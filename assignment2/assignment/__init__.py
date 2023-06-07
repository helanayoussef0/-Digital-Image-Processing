
import numpy as np
from skimage import io

def histogram(image):
    """
    Compute the histogram for an 8-bpc image.
    
    Parameters:
    image (ndarray): An 8-bpc image represented as a numpy array.
    
    Returns:
    hist (ndarray): The computed histogram.
    """
    c = [0] * 256
    if image.dtype != 'uint8':
        raise TypeError("Input image must be an 8-bit image.")
    hist, bins = np.histogram(image, bins=range(257))
    return hist

def apply_lut(image, lut):
    """
    Apply a LUT onto an image.
    
    Parameters:
    image (ndarray): An 8-bpc image represented as a numpy array.
    lut (ndarray): An 8-bit LUT represented as a numpy array.
    
    Returns:
    result (ndarray): The image with the LUT applied.
    """
    if image.dtype != 'uint8':
        raise TypeError("Input image must be an 8-bit image.")
    if len(lut) != 256:
        raise ValueError("LUT must be 256-elements long.")
    result = np.zeros_like(image)
    for i in range(3):
        result[:,:,i] = np.take(lut, image[:,:,i])
    return result

def adjust_brightness(lut, factor):
    """
    Create a LUT that increases/decreases the image brightness.
    
    Parameters:
    lut (ndarray): An empty 8-bit LUT represented as a numpy array.
    factor (float): A factor that determines how much to increase/decrease the brightness.
    
    Returns:
    lut (ndarray): The created LUT.
    """
    for i in range(256):
        value = int(i*factor)
        if value < 0:
            value = 0
        elif value > 255:
            value = 255
        lut[i] = value
    return lut

def adjust_contrast(lut, factor):
    """
    Create a LUT that increases/decreases contrast without changing brightness.
    
    Parameters:
    lut (ndarray): An empty 8-bit LUT represented as a numpy array.
    factor (float): A factor that determines how much to increase/decrease the contrast.
    
    Returns:
    lut (ndarray): The created LUT.
    """
    for i in range(256):
        value = int(128 + factor*(i-128))
        if value < 0:
            value = 0
        elif value > 255:
            value = 255
        lut[i] = value
    return lut

def adjust_exposure(lut, factor):
    """
    Create a LUT that applies a power-law brightness adjustment.
    
    Parameters:
    lut (ndarray): An empty 8-bit LUT represented as a numpy array.
    factor (float): A factor that determines the power-law exponent.
    
    Returns:
    lut (ndarray): The created LUT.
    """
    for i in range(256):
        value = int(255*(i/255)**factor)
        lut[i] = value
    return lut

def log_transform(lut):
    """
    Create a LUT that applies the logarithm transform.
    
    Parameters:
    lut (ndarray): An empty 8-bit LUT represented as a numpy array.
    
    Returns:
    lut (ndarray): The created LUT.
    """
    for i in range(256):
        value = int(255*np.log(1+i)/np.log(256))
        lut[i] = value
    return lut

c = [0] * 256
