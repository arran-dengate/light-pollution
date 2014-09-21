__author__ = 'arran'

import scipy as sp
import math

from scipy import ndimage

def makeStevenKernel(kernelsize):

    if (kernelsize % 2) == 0:
      raise Exception("When calling makekernel method, kernel size should not be even.")

    # The values A and B are constants derived from data.

    A = 1.13
    B = -0.4

    # Create the kernel array and get various dimensions.

    kernel = sp.ones((kernelsize,kernelsize))
    half = (kernelsize-1)/2
    center = ((half),(half))

    for x in range (0, kernel.shape[0]):
      for y in range (0, kernel.shape[1]):
         if (x,y) != center:
            kernel[x][y] = (A*(math.hypot((center[0] - x),(center[1]) - y)) ** B) - 0.108

    print(kernel)

    return kernel


def makeDefaultKernel(kernelsize):

   if (kernelsize % 2) == 0:
      raise Exception("When calling makekernel method, kernel size should not be even.")

   half = (kernelsize-1)/2
   kernel = sp.ones((kernelsize,kernelsize))
   kernel[half][half] = 1
   center = ((half),(half))

   for x in range (0, kernel.shape[0]):
      for y in range (0, kernel.shape[1]):
         if (x,y) != center:
            kernel[x][y] = (1 / (math.hypot((center[0] - x),(center[1]) - y)) ** 1.8) / 5
            # kernel[x][y] = (1 / (math.hypot((center[0] - x),(center[1]) - y) ** 2)) / 28
            # Currently trying an algorithm with less falloff.

   return kernel