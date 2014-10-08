__author__ = 'arran'

from imageprocessing import *
import time
from tkinter import Tk, RIGHT, LEFT, TOP, BOTTOM, BOTH, RAISED, IntVar, Checkbutton, Label, filedialog, NW, S, Entry, StringVar
from tkinter.ttk import Frame, Button, Style

class Window(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()

    def initUI(self):

        self.parent.title("Light pollution map")
        self.style = Style()
        self.style.theme_use("alt")

        self.pack(fill=BOTH, expand=1)

        # Frame for choosing the image

        chooseimageframe = Frame(self, relief=RAISED, borderwidth=1)
        chooseimageframe.pack(fill=BOTH, expand=1)

        chooseimageheader = Label(chooseimageframe, text="Input", font=("Arial", 10, 'bold'))
        chooseimageheader.pack(side=TOP, anchor=NW)

        filelabel = Label(chooseimageframe, text="<None selected>")

        filename = StringVar()

        def choosefile():
            filename.set(filedialog.askopenfilename(parent=chooseimageframe))
            filelabel.config(text=filename.get())

        choosefilebutton = Button(chooseimageframe, text="Choose file...", command=choosefile)
        choosefilebutton.pack(side=LEFT, padx=5, pady=5)
        filelabel.pack(side=LEFT)

        # Frame for clipping options and other preprocessing

        preprocessframe = Frame(self, relief=RAISED, borderwidth=1)
        preprocessframe.pack(fill=BOTH, expand=1)

        preprocessingheader = Label(preprocessframe, text="Preprocessing", font=("Arial", 10, 'bold'))
        preprocessingheader.pack(side=TOP, anchor=NW)

        clippingentryvariable = IntVar()

        clippinglabel = Label(preprocessframe, text="Remove pixels with a value of less than...")
        clippinglabel.pack(side=LEFT)

        clippingentry = Entry(preprocessframe, textvariable=clippingentryvariable, width=4)
        clippingentry.pack(side=LEFT)

        clippingentryvariable.set(value=30)

        # Frame for building the kernel and convolving

        convolveframe = Frame(self, relief=RAISED, borderwidth=1)
        convolveframe.pack(fill=BOTH, expand=1)

        convolveheader = Label(convolveframe, text="Convolve & kernel", font=("Arial", 10, 'bold'))
        convolveheader.pack(side=TOP, anchor=NW)

        kernelsizevariable = IntVar()

        kernelsizelabel = Label(convolveframe, text="Convolve with kernel of size")
        kernelsizelabel.pack(side=LEFT)

        kernelsizeentry = Entry(convolveframe, textvariable=kernelsizevariable, width=4)
        kernelsizeentry.pack(side=LEFT)

        kernelsizevariable.set(value=30)

        # Start button!

        def start():
            print("Filename was " + filename.get())
            processImage()


        startframe = Frame(self, relief=RAISED, borderwidth=1)
        startframe.pack(fill=BOTH, expand=1)

        startbutton = Button(startframe, text="Start!", command=start)
        startbutton.pack(side=LEFT, anchor=S)






def main():

    root = Tk()
    root.geometry("600x400+300+300")
    app = Window(root)
    root.mainloop()

def processImage():

    imagedata = openImage("assets/nsw.jpg")

    imagedata = convolve(imagedata, size=501, type='default')

    imagedata = clip(imagedata, lightClipMinimum=50)
    # imagedata = makeContours(imagedata)
    imagedata = normalise(imagedata)

    saveImage(imagedata)

if __name__ == '__main__':

    start_time = time.time()

    main()

    print("Time taken %d" % (time.time() - start_time))
