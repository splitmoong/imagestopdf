from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import img2pdf

#create a package
win = Tk()

# Set the geometry
win.geometry('750x250')
win.title("Images to PDF")
win.attributes('-alpha',0.85)


def select_file():
    global images
    images = filedialog.askopenfilenames(initialdir="", title="Select Image", filetypes=(("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"), ("All files", "*.*")))
    selected_files_label.config(text="\n".join(images))
    Label(win, text=images).pack()

# Convert Image to PDF
def images_to_pdf():
    if images:
        with open("output.pdf", "wb") as pdf_file:
            pdf_file.write(img2pdf.convert(images))
        Label(frame, text="Saved as output.pdf").pack()


# Add Labels and Buttons
Label(win, text="Image to PDF Converter", font="Caveat 25 bold").pack(pady=30)
ttk.Button(win, text="Select Images", command=select_file).pack(ipadx=10)
frame = Frame(win)
frame.pack()
ttk.Button(frame, text="Convert and Save", command=images_to_pdf).pack(side=LEFT, pady=20, ipadx=10)

ask_output_name = ttk.Entry(win, textvariable="enter the output name of your file")
ask_output_name.pack()

selected_files_label = Label(win, text="", wraplength=600)
selected_files_label.pack()


win.mainloop()