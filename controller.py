__author__ = 'arran'

from imageprocessing import *
import time
from tkinter import Tk, RIGHT, LEFT, TOP, BOTTOM, BOTH, RAISED, IntVar, Checkbutton, Label, filedialog, NW, S, SW, W, \
    N, Entry, StringVar
from tkinter.ttk import Frame, Button, Style

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

        self.pack(fill=BOTH, expand=1)

        padding = {'padx': defaultpadding, 'pady': defaultpadding}

        # Frame for choosing the image

        chooseimageframe = Frame(self, relief=RAISED, borderwidth=1)
        chooseimageframe.pack(fill=BOTH, expand=1)

        chooseimageheader = Label(chooseimageframe, text="Input", font=("Arial", 10, 'bold'))
        chooseimageheader.pack(side=TOP, anchor=NW, **padding)

        filelabel = Label(chooseimageframe, text="<None selected>")

        filenamevariable = StringVar()

        def choosefile():
            filenamevariable.set(filedialog.askopenfilename(parent=chooseimageframe))
            filelabel.config(text=filenamevariable.get())

        choosefilebutton = Button(chooseimageframe, text="Choose file...", command=choosefile)
        choosefilebutton.pack(side=LEFT, **padding)
        filelabel.pack(side=LEFT)

        # Frame for clipping options and other preprocessing

        preprocessframe = Frame(self, relief=RAISED, borderwidth=1)
        preprocessframe.pack(fill=BOTH, expand=1)

        preprocessingheader = Label(preprocessframe, text="Preprocessing", font=("Arial", 10, 'bold'))
        preprocessingheader.pack(side=TOP, anchor=NW, **padding)

        clippingvariable = IntVar()

        clippinglabel = Label(preprocessframe, text="Remove pixels with a value of less than...")
        clippinglabel.pack(side=LEFT, **padding)

        clippingentry = Entry(preprocessframe, textvariable=clippingvariable, width=4)
        clippingentry.pack(side=LEFT, **padding)

        clippingvariable.set(value=defaultclippingvalue)

        # Frame for building the kernel and convolving

        convolveframe = Frame(self, relief=RAISED, borderwidth=1)
        convolveframe.pack(fill=BOTH, expand=1)

        convolveheader = Label(convolveframe, text="Convolve & kernel", font=("Arial", 10, 'bold'))
        convolveheader.pack(side=TOP, anchor=NW, **padding)

        kernelsizevariable = IntVar()

        constant_a_label = Label(convolveframe, text="Constant A:")
        constant_a_label.pack(side=BOTTOM, anchor=SW, **padding)

        constant_a_entry = Entry(convolveframe, textvariable=kernelsizevariable, width=4)
        constant_a_entry.pack(side=BOTTOM, anchor=SW, **padding)

        kernelsizelabel = Label(convolveframe, text="Convolve with kernel of size")
        kernelsizelabel.pack(side=LEFT, anchor=N, **padding)

        kernelsizeentry = Entry(convolveframe, textvariable=kernelsizevariable, width=4)
        kernelsizeentry.pack(side=LEFT, anchor=N, **padding)

        kernelsizevariable.set(value=defaultkernelsize)

        # Start button!

        def start():
            print("Filename was " + filenamevariable.get())
            processimage(filename=filenamevariable.get(), kernelsize=kernelsizevariable.get(),
                         clippingvalue=clippingvariable.get())

        controlframe = Frame(self, relief=RAISED, borderwidth=1)
        controlframe.pack(fill=BOTH, expand=1)

        controlheader = Label(controlframe, text="Control", font=("Arial", 10, 'bold'))
        controlheader.pack(side=TOP, anchor=NW, **padding)

        startbutton = Button(controlframe, text="Start!", command=start)
        startbutton.pack(side=LEFT, **padding)

        quitbutton = Button(controlframe, text="Quit", command=quit)
        quitbutton.pack(side=LEFT, **padding)


def main():

    root = Tk()
    root.geometry("600x450+300+300")
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