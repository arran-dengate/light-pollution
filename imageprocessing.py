__author__ = 'arran'
from PIL import Image
import numpy as np
import scipy as sp
import scipy.signal as sig
import matplotlib.image as mpimg
import math
import time

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

def save_image(imagedata, filename):

    print('Saving image...')

    # Convert array back into image.
    final_image = Image.fromarray(imagedata)

    # Convert it back to RGB and save to JPG.
    final_image = final_image.convert("RGB")
    final_image.save(filename + ".png")

    print('Saving image complete.')

def convolve(imagedata, kernel_size, a, b, c):

    if (kernel_size % 2) == 0:
      raise Exception("When calling makekernel method, kernel size should not be even.")

    kernel = sp.ones((kernel_size,kernel_size))
    half = (kernel_size-1)/2
    center = ((half),(half))

    print(kernel_size, a, b, c)

    # The polynomial for the kernel falloff is Ax ^ B - C.
    # In this, A B and C are constants, x is the hypotenuse.

    for x in range (0, kernel.shape[0]):
      for y in range (0, kernel.shape[1]):
         if (x,y) != center:
            kernel[x][y] = (a*(math.hypot((center[0] - x),(center[1]) - y)) ** b) - c

    print('Starting convolve...')
    imagedata = sig.fftconvolve(imagedata, kernel, mode="same")
    print('Completed convolve.')

    return imagedata


def make_contours(scale_values_list):

    imagedata = open_image("processed_image.png")

    # Apply contours

    print('Starting contours...')

    print(scale_values_list)
    scale_values_list.insert(0,0) # Ensure that first contour is zero.

    counter = 0

    start_time = time.time()

    for x in range(0,imagedata.shape[0]):
        for y in range(0, imagedata.shape[1]):
            value = imagedata[x][y]
            global counter
            counter = 0
            while counter < len(scale_values_list):
                if value < scale_values_list[counter]:
                    global counter
                    imagedata[x][y] = scale_values_list[counter-1]
                    counter = 12

                global counter
                counter+=1

    print("Time taken: %d seconds" % (time.time() - start_time))

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
