import numpy as np

def imread(filename: str) -> np.ndarray:
    '''Load a NetPBM image from a file.

    Parameters
    ----------
    filename : str
        image file name

    Returns
    -------
    numpy.ndarray
        a numpy array with the loaded image

    Raises
    ------
    ValueError
        if the image format is unknown or invalid
    '''
    with open(filename, 'rt') as f:
        contents = f.read()
    # Split the file contents into its constituent tokens.
    tokens = contents.split()
    if tokens[0] == 'P2':
        # Get the image dimensions.
        width = int(tokens[1])
        height = int(tokens[2])
        maxval = int(tokens[3])
        # Convert all of the string tokens into integers.
        values = [int(token) for token in tokens[4:]]
        if maxval != 255:
            raise ValueError(f'Can only support 8-bit images.')
        # Create the numpy array, reshaping it so that it's no longer a linear array.
        image = np.array(values, dtype=np.uint8)
        return np.reshape(image, (height, width))
    elif tokens[0] == 'P3':
        # Get the image dimensions.
        width = int(tokens[1])
        height = int(tokens[2])
        maxval = int(tokens[3])
        # Convert all of the string tokens into integers.
        values = [int(token) for token in tokens[4:]]
        if maxval != 255:
            raise ValueError(f'Can only support 8-bit images.')
        # Create the numpy array, reshaping it so that it's no longer a linear array.
        image = np.array(values, dtype=np.uint8)
        return np.reshape(image, (height, width, 3))
    else:
        raise ValueError(f'Unknown format {tokens[0]}')


def imwrite(filename: str, image: np.ndarray):
    '''Save a NetPBM image to a file.

    Parameters
    ----------
    filename : str
        image file name
    image : numpy.ndarray
        image being saved
    '''
    # Extract the image dimensions and check that it's 8bpc
    height, width = image.shape[:2]
    if image.dtype != np.uint8:
        raise ValueError('Can only support 8-bit images.')
    if image.ndim == 2:
        # Convert the image values to strings.
        values = image.astype(str)
        # Construct the file contents.
        rows = [' '.join(row) for row in values]
        header = '\n'.join(['P2', str(width), str(height), '255'])
        data = '\n'.join(rows)
        # Write it to a file.
        with open(filename, 'wt') as f:
            f.write(header)
            f.write('\n')
            f.write(data)
