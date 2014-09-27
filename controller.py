__author__ = 'arran'

from imageprocessing import *
import time
from tkinter import Tk, BOTH
from tkinter.ttk import Frame, Button, Style

class Window(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()

    def initUI(self):

        self.parent.title("Light pollution map helper")

        self.pack(fill=BOTH, expand=1)

        self.style = Style()
        self.style.theme_use("clam")

        self.quitButton = Button(self, text="Quit", command=self.quit)
        self.quitButton.place(x=50, y=50)
        self.quitButton.place(x=50, y=50)

        self.style.configure("TFrame", background="#333")


def main():

    root = Tk()
    root.geometry("450x450+200+200")
    app = Window(root)
    root.mainloop()

    quit()

    imagedata = openImage("assets/nsw.jpg")

    imagedata = convolve(imagedata, size=501, type='Steven')

    imagedata = clip(imagedata, lightClipMinimum=50)
    # imagedata = makeContours(imagedata)
    imagedata = normalise(imagedata)

    saveImage(imagedata)



if __name__ == '__main__':

    start_time = time.time()

    main()

    print("Time taken %d" % (time.time() - start_time))
