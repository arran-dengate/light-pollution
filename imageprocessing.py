__author__ = 'arran'
from PIL import Image
import numpy as np
import scipy as sp
import scipy.signal as sig
import kernel
import matplotlib.image as mpimg

def openImage(filepath):

    # Open image, convert to greyscale, then import into a SciPy array.

    im = Image.open(filepath)
    original_image = im.copy()
    original_image = original_image.convert("L")
    im = im.convert("L")

    original_image.save('greyscale.jpg')

    img = mpimg.imread('greyscale.jpg')
    print(img)

    imagedata = sp.array(img)

    return imagedata

def saveImage(imagedata):

    # Convert array back into image.
    final_image = Image.fromarray(imagedata)

    # Convert it back to RGB and save to JPG.
    final_image = final_image.convert("RGB")
    final_image.save('final_image.png')

def convolve(imagedata, size=2001, type='default'):

    if type == 'default':

        print('Starting convolve...')
        imagedata = sig.fftconvolve(imagedata, kernel.makeDefaultKernel(size), mode="same")
        print('Completed convolve.')

    elif type == 'Steven':

        print('Starting convolve...')
        imagedata = sig.fftconvolve(imagedata, kernel.makeStevenKernel(size), mode="same")
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

def clip(imagedata, lightClipMinimum = 50):

    # Cut out terrain (by reducing anything with less than a certain brightness value to zero).

    imagedata[imagedata < lightClipMinimum] = 0

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
