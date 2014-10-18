__author__ = 'arran'
from PIL import Image
import numpy as np
import scipy as sp
import scipy.signal as sig
import kernel
import matplotlib.image as mpimg

def open_image(filepath):

    # Open image, convert to greyscale, then import into a SciPy array.

    im = Image.open(filepath)
    original_image = im.copy()
    original_image = original_image.convert("L")
    im = im.convert("L")

    original_image.save('greyscale.jpg')

    img = mpimg.imread('greyscale.jpg')

    imagedata = sp.array(img)

    return imagedata

def save_image(imagedata):

    print('Saving image...')

    # Convert array back into image.
    final_image = Image.fromarray(imagedata)

    # Convert it back to RGB and save to JPG.
    final_image = final_image.convert("RGB")
    final_image.save('final_image.png')

    print('Saving image complete.')

def convolve(imagedata, size, type='default'):

    if type == 'default':

        print('Starting convolve with kernel size ' + str(size))
        imagedata = sig.fftconvolve(imagedata, kernel.make_default_kernel(size, constant_a=1.13, constant_b=-0.4,
                                                                          constant_c=-0.108), mode="same")
        print('Completed convolve.')

    elif type == 'alternate':

        print('Starting convolve...')
        imagedata = sig.fftconvolve(imagedata, kernel.make_alternate_kernel(size), mode="same")
        print('Completed convolve.')



    return imagedata

def makeContours(imagedata):

    # Apply contours

    print('Starting contours...')

    contour1 = 5
    contour2 = 7
    contour3 = 10
    contour4 = 20
    contour5 = 30
    contour6 = 40
    contour7 = 60
    contour8 = 100
    contour9 = 200
    max = 255

    value = 0

    for x in range (0,imagedata.shape[0]):
      for y in range (0, imagedata.shape[1]):
         value = imagedata[x][y]
         if value < contour1:
            imagedata[x][y] = 0
         elif value < contour2:
            imagedata[x][y] = contour1
         elif value < contour3:
            imagedata[x][y] = contour2
         elif value < contour4:
            imagedata[x][y] = contour3
         elif value < contour5:
            imagedata[x][y] = contour4
         elif value < contour6:
            imagedata[x][y] = contour5
         elif value < contour7:
            imagedata[x][y] = contour6
         elif value < contour8:
            imagedata[x][y] = contour7
         elif value < contour9:
            imagedata[x][y] = contour8
         else:
            imagedata[x][y] = max

    print('Completed contours.')

    return imagedata

def clip(imagedata, lightclipminimum = 50):

    # Cut out terrain (by reducing anything with less than a certain brightness value to zero).

    print('Starting clipping with value ' + str(lightclipminimum))

    imagedata[imagedata < lightclipminimum] = 0

    return imagedata

def normalise(imagedata):

    # Scale the values in the image so the highest value is 255.

    imageBrightestPoint = np.amax(imagedata)
    normalisationScaleValue = 255 / imageBrightestPoint

    if imageBrightestPoint > 255:
        print('Starting normalisation...')

        for x in range (0,imagedata.shape[0]):
            for y in range (0, imagedata.shape[1]):
                imagedata[x][y] *= normalisationScaleValue

        print('Completed normalisation.')

    else: print('Normalisation not needed.')

    return imagedata
