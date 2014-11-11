__author__ = 'arran'

from imageprocessing import *
import time
from tkinter import Tk, RIGHT, LEFT, TOP, BOTTOM, BOTH, RAISED, IntVar, DoubleVar, Checkbutton, Label, filedialog, NW, \
    S, SW, W, N, E, Entry, StringVar, Canvas, PhotoImage, CENTER, LEFT, RIGHT, Scale, HORIZONTAL
from tkinter.ttk import Frame, Button, Style
from PIL import Image, ImageTk

# Default variable values

default_kernel_size = 501
default_clipping_value = 30
default_constant_a = 1.13
default_constant_b = -0.4
default_constant_c = 0.108

# Default GUI values

defaultpadding = 5
canvas_size = 350    # Used in import and export frames

class Window(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.grid(sticky=N+E+S+W)

        self.initui()

    def initui(self):

        self.parent.title("Light pollution map")
        self.style = Style()
        self.style.theme_use("alt")

        self.grid(row=0, column=0)

        padding = {'padx':'5', 'pady':'5'}
        big_heading_font = ("Arial", 14, 'bold')
        small_heading_font = ("Arial", 10, 'bold')

        # Create frames.
        # There are three frames for settings - preprocessing, convolve, and contour.
        # Each also has an image frame underneath it.
        # Layout is as follows:
        #
        #             --------------------------------------------------------------------------
        #             |                 |                 |                 |                  |
        #             |                 |                 |                 |                  |
        #             |   import_body   |   process_body  |   contour_body  |   export_body    |
        #             |                 |                 |                 |                  |
        #             |                 |                 |                 |                  |
        #             --------------------------------------------------------------------------

        # Settings frames

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        import_body = Frame(self, relief=RAISED, borderwidth=1)
        import_body.grid(row=0, column=0, sticky=N+S+E+W)

        process_body = Frame(self, relief=RAISED, borderwidth=1)
        process_body.grid(row=0, column=1, sticky=N+S+E+W)

        contour_body = Frame(self, relief=RAISED, borderwidth=1)
        contour_body.grid(row=0, column=2, sticky=N+S+E+W)

        export_body = Frame(self, relief=RAISED, borderwidth=1)
        export_body.grid(row=0, column=3, sticky=N+S+E+W)

         # =============================================================================================================
        #
        # Contents of load_image_frame
        #
        # =============================================================================================================

        # Heading

        processing_frame_header = Label(import_body, text="Import", font=big_heading_font)
        processing_frame_header.grid(row=0, column=0, sticky=N, **padding)

        filename_variable = StringVar()

        # Import image

        import_canvas = Canvas(import_body, width=canvas_size, height=canvas_size, background='black')
        import_canvas.grid(row=1, column=0, sticky=N, **padding)

        # Load file method

        def choosefile():
            filename_variable.set(filedialog.askopenfilename(parent=import_body))
            image = Image.open(filename_variable.get())
            thumbnail = create_thumbnail(image, canvas_size)
            import_canvas.create_image(0, 0, image=thumbnail, anchor=NW)

        load_image_button = Button(import_body, text="Import image", command=choosefile)
        load_image_button.grid(row=2, column=0, columnspan=2, sticky=E+W+S, **padding)
        import_body.rowconfigure(2, weight=1)

        # =============================================================================================================
        #
        # Contents of processing_frame
        #
        # =============================================================================================================

        processing_frame_header = Label(process_body, text="Process", font=big_heading_font)
        processing_frame_header.grid(row=0, column=0, columnspan=2, sticky=N, **padding)

        clipping_variable = IntVar()

        constants_label = Label(process_body, text="Clipping",
                                font=("Arial", 10, 'bold'))
        constants_label.grid(row=1, column=0, sticky=E, **padding)

        clipping_label = Label(process_body, text="Remove pixels with \n brightness under")
        clipping_label.grid(row=2, column=0, sticky=E, **padding)

        clipping_entry = Entry(process_body, textvariable=clipping_variable, width=4)
        clipping_entry.grid(row=2, column=1, sticky=W, **padding)

        clipping_variable.set(value=default_clipping_value)

        convolve_header = Label(process_body, text="Kernel", font=small_heading_font)
        convolve_header.grid(row=4, column=0, sticky=E, **padding)

        kernel_size_variable = IntVar()

        kernel_size_label = Label(process_body, text="Convolve kernel size", justify=RIGHT)
        kernel_size_label.grid(row=5, column=0, sticky=E, **padding)

        kernel_size_entry = Entry(process_body, textvariable=kernel_size_variable, width=4)
        kernel_size_entry.grid(row=5, column=1, sticky=W, **padding)
        kernel_size_variable.set(value=default_kernel_size)

        # Constants for convolve equation

        constants_label = Label(process_body, text="Falloff",
                                font=("Arial", 10, 'bold'))
        constants_label.grid(row=6, column=0, sticky=E, **padding)

        constant_a_label = Label(process_body, text="Constant A:")
        constant_b_label = Label(process_body, text="Constant B:")
        constant_c_label = Label(process_body, text="Constant C:")

        constant_a_label.grid(row=7, column=0, sticky=E, **padding)
        constant_b_label.grid(row=8, column=0, sticky=E, **padding)
        constant_c_label.grid(row=9, column=0, sticky=E, **padding)

        constant_a_variable = DoubleVar()
        constant_b_variable = DoubleVar()
        constant_c_variable = DoubleVar()

        constant_a_entry = Entry(process_body, textvariable=constant_a_variable, width=4)
        constant_b_entry = Entry(process_body, textvariable=constant_b_variable, width=4)
        constant_c_entry = Entry(process_body, textvariable=constant_c_variable, width=4)

        constant_a_variable.set(default_constant_a)
        constant_b_variable.set(default_constant_b)
        constant_c_variable.set(default_constant_c)

        constant_a_entry.grid(row=7, column=1, **padding)
        constant_b_entry.grid(row=8, column=1, **padding)
        constant_c_entry.grid(row=9, column=1, **padding)

        constants_note = Label(process_body, text="Falloff equation is (Ax^B)-C", font=("Arial", 9))
        constants_note.grid(row=10, column=0, columnspan=2, sticky=E, **padding)

        # Start button!

        def process():
            print("Filename was " + filename_variable.get())
            image_data =  process_image(filename=filename_variable.get(),
                                        kernel_size=kernel_size_variable.get(),
                                        clipping_value=clipping_variable.get(),
                                        constant_a=constant_a_variable.get(),
                                        constant_b=constant_b_variable.get(),
                                        constant_c=constant_c_variable.get()
                                        )

            image_data = Image.open("processed_image.png")
            thumbnail = create_thumbnail(image_data, canvas_size)
            export_canvas.create_image(0, 0, image=thumbnail, anchor=NW)

        start_button = Button(process_body, text="Process image", command=process)
        start_button.grid(row=11, column=0, columnspan=3, sticky=E+W+S, **padding)
        process_body.rowconfigure(11, weight=1)

        # =============================================================================================================
        #
        # Contents of contour_frame
        #
        # =============================================================================================================

        contour_header = Label(contour_body, text="Contour", font=big_heading_font)
        contour_header.grid(row=0, column=0, sticky=S, columnspan=2, **padding)

        contour_note = Label(contour_body, text="(optional)")
        contour_note.grid(row=1, column=0, sticky=S, columnspan=2)

        scale_options = {"width":"5", "length":"150"}
        slider_padding = {"padx":"2", "pady":"0"}

        scale_list = []
        scale_values_list = []

        default_scale_values = [5, 7, 10, 20, 30, 40, 60, 100, 200]

        for i in range(9):
            scale = Scale(contour_body, from_=0, to_=255, orient=HORIZONTAL, **scale_options)
            scale.grid(row=i+2, column=0, columnspan=2, sticky=S, **slider_padding)
            scale.set(default_scale_values[i])
            scale_list.append(scale)

        for scale in scale_list:
            print(scale)
            print(type(scale))
            #print(scale.get())

        def contour():

            scale_values_list.clear()

            for scale in scale_list:
                scale_values_list.append(scale.get())

            contour_image(scale_values_list)

            image_data = Image.open("Contoured_image.png")
            thumbnail = create_thumbnail(image_data, canvas_size)
            export_canvas.create_image(0, 0, image=thumbnail, anchor=NW)

        contour_button = Button(contour_body, text="Contour image", command=contour)
        contour_button.grid(row=11, column=0, columnspan=2, sticky=E+S+W, **padding)
        contour_body.rowconfigure(11, weight=1)
        contour_body.columnconfigure(1, weight=1)

        # =============================================================================================================
        #
        # Contents of export_body
        #
        # =============================================================================================================

        filename_export_variable = StringVar()

        def export_file():
            filename_options = {}
            filename_options['filetypes'] = [('PNG', '.png')]
            filename_options['initialfile'] = 'output.png'
            filename_options['parent'] = self
            filename_export_variable.set(filedialog.asksaveasfilename(**filename_options))
            image_data = Image.open("Contoured_image.png")
            image_data.save(filename_export_variable.get())

        export_header = Label(export_body, text="Export", font=big_heading_font)
        export_header.grid(row=0, column=0, sticky=N, **padding)

        export_canvas = Canvas(export_body, width=canvas_size, height=canvas_size, background='black')
        export_canvas.grid(row=1, column=0, **padding)

        export_button = Button(export_body, text="Export image", command=export_file)
        export_button.grid(row=2, column=0, columnspan=2, sticky=E+W+S, **padding)
        export_body.rowconfigure(2, weight=1)



def main():

    root = Tk()
    root.geometry("1100x450+300+300")
    root.resizable(width=False,height=False)
    app = Window(root)
    root.mainloop()

def create_thumbnail(image, thumbnail_size):

    (width, height) = image.size
    print(width, height)
    resize_ratio = (min(thumbnail_size/width, thumbnail_size/height))
    image.thumbnail((width*resize_ratio, height*resize_ratio), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    photo_label = Label(image=photo)
    photo_label.image = photo

    return photo

def process_image(filename, kernel_size, clipping_value, constant_a, constant_b, constant_c):

    start_time = time.time()

    image_data = open_image(filename)

    image_data = convolve(image_data, kernel_size=kernel_size, a=constant_a, b=constant_b, c=constant_c)

    image_data = clip(image_data, lightclipminimum=clipping_value)
    # image_data = makeContours(image_data)
    image_data = normalise(image_data)

    save_image(image_data, filename="processed_image")

    # Create thumbnail of image.

    return image_data

    print("Time taken: %d seconds" % (time.time() - start_time))

def contour_image(contour_levels):

    contour_result = make_contours(contour_levels)
    save_image(contour_result, filename="Contoured_image")

if __name__ == '__main__':

    main()