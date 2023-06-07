import argparse
import numpy as np
from PIL import Image

def histogram(image):
    """
    Computes the histogram of an 8-bit image.

    Parameters:
        image (PIL.Image.Image): The input image.

    Returns:
        np.ndarray: The histogram of the image.
    """
    # Convert the image to grayscale and flatten it
    image = image.convert('L')
    pixels = np.array(image).flatten()

    # Compute the histogram
    histogram = np.zeros(256, dtype=np.uint32)
    for pixel in pixels:
        histogram[pixel] += 1

    return histogram

def cdf(cumulative_dist):
    """
    Computes the cumulative distribution function (CDF) of a histogram.

    Parameters:
        cumulative_dist (np.ndarray): The input histogram.

    Returns:
        np.ndarray: The CDF of the histogram.
    """
    # Compute the PDF and normalize it
    pdf = cumulative_dist / float(cumulative_dist.sum())

    # Compute the CDF
    cdf_array = np.zeros_like(pdf)
    cdf_array[0] = pdf[0]
    for i in range(1, 256):
        cdf_array[i] = cdf_array[i-1] + pdf[i]

    return cdf_array

def equalize(image):
    """
    Performs histogram equalization on an 8-bit grayscale image.

    Parameters:
        image (PIL.Image.Image): The input image.

    Returns:
        PIL.Image.Image: The equalized image.
    """
    # Compute the histogram and CDF
    hist = histogram(image)
    cumulative_dist = cdf(hist)

    # Compute the LUT
    lut = np.uint8(255 * cumulative_dist)

    # Apply the LUT to the image
    equalized = image.point(lut)

    return equalized

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='input image file name')
    parser.add_argument('output', help='output image file name')
    args = parser.parse_args()

    # Load the input image
    image = Image.open(args.input)

    # Convert the image to grayscale if it's color
    if image.mode != 'L':
        image = image.convert('L')

    # Equalize the image
    equalized = equalize(image)

    # Save the equalized image
    equalized.save(args.output)

