__author__ = 'arran'

from imageprocessing import *
import time
from tkinter import Tk, RIGHT, LEFT, TOP, BOTTOM, BOTH, RAISED, IntVar, Checkbutton, Label, filedialog, NW, S, SW, W, \
    N, E, Entry, StringVar, Canvas, PhotoImage, CENTER
from tkinter.ttk import Frame, Button, Style
from PIL import Image, ImageTk

# Default variable values

defaultkernelsize = 501
defaultclippingvalue = 30

# Default GUI values

defaultpadding = 5

class Window(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initui()

    def initui(self):

        self.parent.title("Light pollution map")
        self.style = Style()
        self.style.theme_use("alt")

        self.grid(row=0, column=0)

        padding = {'padx':'5', 'pady':'5'}

        # Images

        original_image_frame = Frame(self, relief=RAISED, borderwidth=1)
        original_image_frame.grid(row=0, column=0, rowspan=8, columnspan=8, sticky=N+S+E+W)

        canvas = Canvas(original_image_frame, width=200, height=200)
        canvas.grid(row=8, column=8)

        image = Image.open('assets/act.jpg')
        image.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image)

        photolabel = Label(image=photo)
        photolabel.image = photo

        canvas.create_image(0,0,image=photo, anchor=CENTER)

        # Frame for choosing the image

        chooseimageframe = Frame(self, relief=RAISED, borderwidth=1)
        chooseimageframe.grid(row=9, column=0, rowspan=8, columnspan=7, sticky=N+S)

        chooseimageheader = Label(chooseimageframe, text="Original", font=("Arial", 10, 'bold'))
        chooseimageheader.grid(row=9, column=0, **padding)

        filelabel = Label(chooseimageframe, text="<None selected>")

        filenamevariable = StringVar()

        def choosefile():
            filenamevariable.set(filedialog.askopenfilename(parent=chooseimageframe))
            filelabel.config(text=filenamevariable.get())

        choosefilebutton = Button(chooseimageframe, text="Choose image file...", command=choosefile)
        choosefilebutton.grid(row=10, column=0, **padding)
        filelabel.grid(row=10, column=1, **padding)



        # Frame for clipping options and other preprocessing

        processframe = Frame(self, relief=RAISED, borderwidth=1)
        processframe.grid(row=9, column=9, rowspan=8, columnspan=7, sticky=N+S)

        preprocessingheader = Label(processframe, text="Processing", font=("Arial", 10, 'bold'))
        preprocessingheader.grid(row=9, column=9, **padding)

        clippingvariable = IntVar()

        clippinglabel = Label(processframe, text="Remove pixels with a value of less than...")
        clippinglabel.grid(row=10, column=9, **padding)

        clippingentry = Entry(processframe, textvariable=clippingvariable, width=4)
        clippingentry.grid(row=10, column=10, **padding)

        clippingvariable.set(value=defaultclippingvalue)

        # Frame for building the kernel and convolving

        preprocessingheader = Label(processframe, text="Convolve kernel", font=("Arial", 10, 'bold'))
        preprocessingheader.grid(row=11, column=9, **padding)

        kernelsizevariable = IntVar()

        kernelsizelabel = Label(processframe, text="Convolve with kernel of size")
        kernelsizelabel.grid(row=12, column=9, **padding)

        kernelsizeentry = Entry(processframe, textvariable=kernelsizevariable, width=4)
        kernelsizeentry.grid(row=12, column=10, **padding)
        kernelsizevariable.set(value=defaultkernelsize)

        constant_a_label = Label(processframe, text="Constant A:")
        constant_a_label.grid(row=13, column=9, **padding)

        constant_a_variable = IntVar()

        constant_a_entry = Entry(processframe, textvariable=constant_a_variable, width=4)
        constant_a_entry.grid(row=13, column=10, **padding)

        # Start button!

        def start():
            print("Filename was " + filenamevariable.get())
            processimage(filename=filenamevariable.get(), kernelsize=kernelsizevariable.get(),
                         clippingvalue=clippingvariable.get())

        startbutton = Button(processframe, text="Start processing", command=start)
        startbutton.grid(row=14, column=9, sticky=S, **padding)

        # Contour frame

        contour_frame = Frame(self, relief=RAISED, borderwidth=1)
        contour_frame.grid(row=9, column=17, rowspan=8, columnspan=8, sticky=N+S)

        contour_header = Label(contour_frame, text="Contour", font=("Arial", 10, 'bold'))
        contour_header.grid(row=9, column=17, **padding)





def main():

    root = Tk()
    root.geometry("700x450+300+300")
    app = Window(root)
    root.mainloop()

def processimage(filename, kernelsize, clippingvalue):

    start_time = time.time()

    imagedata = openImage(filename)

    imagedata = convolve(imagedata, size=kernelsize, type='default')

    imagedata = clip(imagedata, lightclipminimum=clippingvalue)
    # imagedata = makeContours(imagedata)
    imagedata = normalise(imagedata)

    saveImage(imagedata)

    print("Time taken: %d seconds" % (time.time() - start_time))

if __name__ == '__main__':

    main()