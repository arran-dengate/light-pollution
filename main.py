__author__ = 'arran'
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
im = Image.open("assets/australia_night_201204-10_lrg-cropped.jpg")
import numpy as np
import scipy as sp
import scipy.signal as sig
import kernelmaker

original_image = im.copy()
original_image = original_image.convert("L")

im = im.convert("L")

original_image.save('original_image.jpg')

imagewidth = im.size[0]
imageheight = im.size[1]

imagedata = sp.zeros((imagewidth, imageheight))

print(im.getextrema())

for x in range (0,imagewidth):
   for y in range (0, imageheight):
      imagedata[x][y] = im.getpixel((x,y))

print(imagedata)

print('Starting convolve...')
imagedata = sig.fftconvolve(imagedata, kernelmaker.makekernel(151), mode="same")
# imagedata = kernelmaker.convolve(imagedata, kernelmaker.makekernel(151))
print('Completed convolve.')

final_image = Image.fromarray(imagedata)

final_image = final_image.rotate(angle=-90)
final_image = final_image.transpose(Image.FLIP_LEFT_RIGHT)

final_image = final_image.convert("RGB")
#enhancer = ImageEnhance.Brightness(final_image)
#final_image = enhancer.enhance(4.0)
final_image.save('final_image.jpg')