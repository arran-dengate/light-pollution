__author__ = 'arran'

from imageprocessing import *
import time
import tkinter as tk

class Window(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.initUI()

    def initUI(self):

        self.parent.title("Light pollution map helper")

        self.pack(expand=1)



        self.quitButton = tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.place(x=50, y=50)
        self.quitButton.pack(side="bottom")


def main():

    root = tk.Tk()
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
