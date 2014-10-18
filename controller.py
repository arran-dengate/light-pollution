__author__ = 'arran'

from imageprocessing import *
import time
from tkinter import Tk, RIGHT, LEFT, TOP, BOTTOM, BOTH, RAISED, IntVar, Checkbutton, Label, filedialog, NW, S, SW, W, \
    N, E, Entry, StringVar, Canvas, PhotoImage, CENTER, LEFT, RIGHT
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
        big_heading_font = ("Arial", 14, 'bold')
        small_heading_font = ("Arial", 10, 'bold')

        # Images

        original_image_frame = Frame(self, relief=RAISED, borderwidth=1)
        original_image_frame.grid(row=1, column=0, sticky=N+S+E+W)

        convolved_image_frame = Frame(self, relief=RAISED, borderwidth=1)
        convolved_image_frame.grid(row=1, column=1, sticky=N+S+E+W)

        contoured_image_frame = Frame(self, relief=RAISED, borderwidth=1)
        contoured_image_frame.grid(row=1, column=2, sticky=N+S+E+W)

        original_canvas = Canvas(original_image_frame, width=250, height=250)
        original_canvas.pack(**padding)

        convolved_canvas = Canvas(convolved_image_frame, width=250, height=250)
        convolved_canvas.pack(**padding)

        contoured_canvas = Canvas(contoured_image_frame, width=250, height=250)
        contoured_canvas.pack(**padding)

        image = Image.open('assets/act.jpg')
        image.thumbnail((250, 250))
        photo = ImageTk.PhotoImage(image)

        photo_label = Label(image=photo)
        photo_label.image = photo

        original_canvas.create_image(0,0,image=photo, anchor=CENTER)

        # Frame for choosing the image

        choose_image_frame = Frame(self, relief=RAISED, borderwidth=1)
        choose_image_frame.grid(row=0, column=0, sticky=N+S+E+W)

        processing_frame_header = Label(choose_image_frame, text="Preprocessing", font=big_heading_font)
        processing_frame_header.grid(row=0, column=0, sticky=E, **padding)

        filename_variable = StringVar()

        preprocessing_header = Label(choose_image_frame, text="Clipping settings", font=small_heading_font)
        preprocessing_header.grid(row=4, column=0, sticky=E, **padding)

        clipping_variable = IntVar()

        clipping_label = Label(choose_image_frame, text="Remove pixels with brightness under")
        clipping_label.grid(row=5, column=0, sticky=E, **padding)

        clipping_entry = Entry(choose_image_frame, textvariable=clipping_variable, width=4)
        clipping_entry.grid(row=5, column=1, sticky=W, **padding)

        clipping_variable.set(value=defaultclippingvalue)

        # Load file

        def choosefile():
            filename_variable.set(filedialog.askopenfilename(parent=choose_image_frame))

        load_image_button = Button(choose_image_frame, text="Load image", command=choosefile)
        load_image_button.grid(row=6, column=0, columnspan=2, sticky=E+W+S, **padding)
        choose_image_frame.rowconfigure(6, weight=1)



        # Frame for processing tasks (clipping, convolve)

        process_frame = Frame(self, relief=RAISED, borderwidth=1)
        process_frame.grid(row=0, column=1, sticky=N+S+E+W)

        processing_frame_header = Label(process_frame, text="Convolve", font=big_heading_font)
        processing_frame_header.grid(row=0, column=0, sticky=E, **padding)

        convolve_header = Label(process_frame, text="Kernel settings", font=small_heading_font)
        convolve_header.grid(row=3, column=0, sticky=E, **padding)

        kernel_size_variable = IntVar()

        kernel_size_label = Label(process_frame, text="Convolve with kernel of size", justify=RIGHT)
        kernel_size_label.grid(row=4, column=0, sticky=E, **padding)

        kernel_size_entry = Entry(process_frame, textvariable=kernel_size_variable, width=4)
        kernel_size_entry.grid(row=4, column=1, sticky=W, **padding)
        kernel_size_variable.set(value=defaultkernelsize)

        # Constants for convolve equation

        constants_label = Label(process_frame, text="Falloff settings",
                                font=("Arial", 10, 'bold'))
        constants_label.grid(row=5, column=0, sticky=E, **padding)

        constant_a_label = Label(process_frame, text="Constant A:")
        constant_b_label = Label(process_frame, text="Constant B:")
        constant_c_label = Label(process_frame, text="Constant C:")

        constant_a_label.grid(row=6, column=0, sticky=E, **padding)
        constant_b_label.grid(row=7, column=0, sticky=E, **padding)
        constant_c_label.grid(row=8, column=0, sticky=E, **padding)

        constant_a_variable = IntVar()
        constant_b_variable = IntVar()
        constant_c_variable = IntVar()

        constant_a_entry = Entry(process_frame, textvariable=constant_a_variable, width=4)
        constant_b_entry = Entry(process_frame, textvariable=constant_b_variable, width=4)
        constant_c_entry = Entry(process_frame, textvariable=constant_c_variable, width=4)

        constant_a_entry.grid(row=6, column=1, **padding)
        constant_b_entry.grid(row=7, column=1, **padding)
        constant_c_entry.grid(row=8, column=1, **padding)

        constants_note = Label(process_frame, text="Falloff equation is (Ax^B)-C", font=("Arial", 9))
        constants_note.grid(row=9, column=0, columnspan=2, sticky=E, **padding)

        # Start button!

        def start():
            print("Filename was " + filename_variable.get())
            process_image(filename=filename_variable.get(), kernel_size=kernel_size_variable.get(),
                         clipping_value=clipping_variable.get())

        start_button = Button(process_frame, text="Start processing", command=start)
        start_button.grid(row=10, column=0, columnspan=2, sticky=E+W, **padding)

        # Contour frame

        contour_frame = Frame(self, relief=RAISED, borderwidth=1)
        contour_frame.grid(row=0, column=2, sticky=N+S+E+W)

        contour_header = Label(contour_frame, text="Contour", font=big_heading_font)
        contour_header.grid(row=0, column=0, sticky=N, columnspan=2, **padding)





def main():

    root = Tk()
    root.geometry("900x550+300+300")
    app = Window(root)
    root.mainloop()

def process_image(filename, kernel_size, clipping_value):

    start_time = time.time()

    image_data = open_image(filename)

    image_data = convolve(image_data, size=kernel_size, type='default')

    image_data = clip(image_data, lightclipminimum=clipping_value)
    # image_data = makeContours(image_data)
    image_data = normalise(image_data)

    save_image(image_data)

    print("Time taken: %d seconds" % (time.time() - start_time))

if __name__ == '__main__':

    main()