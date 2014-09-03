__author__ = 'arran'

import scipy as sp
import math

from scipy import ndimage

def normalisekernel (anarray):
    sum = 0
    for x in range (0, anarray.shape[0]):
        for y in range (0, anarray.shape[1]):
            sum += anarray[x][y]

    print('Sum was ' + str(sum))

    for x in range (0, anarray.shape[0]):
        for y in range (0, anarray.shape[1]):
            anarray[x][y] = anarray[x][y] / sum

    return anarray

def makekernel(kernelsize):

   if (kernelsize % 2) == 0:
      raise Exception("When calling makekernel method, kernel size should not be even.")

   half = (kernelsize-1)/2
   kernel = sp.ones((kernelsize,kernelsize))
   kernel[half][half] = 1
   center = ((half),(half))

   for x in range (0, kernel.shape[0]):
      for y in range (0, kernel.shape[1]):
         if (x,y) != center:
            kernel[x][y] = (1 / (math.hypot((center[0] - x),(center[1]) - y) ** 2) * 10) / 100
            # kernel[x][y] = (1 / (math.hypot((center[0] - x),(center[1]) - y) ** 2)) / 28
            # Currently trying an algorith with less falloff.

   return kernel

def main():

   sp.set_printoptions(precision=2, suppress=True)

   kernel = makekernel(9)

   print(kernel)


   testdata = sp.ones((14,14))
   testdata[7][7] = 30
   print(testdata)

   result = ndimage.convolve(testdata, kernel)

   sp.set_printoptions(precision=2)
   print(result)

if __name__ == '__main__':
   main()