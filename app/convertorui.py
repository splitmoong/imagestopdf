from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ExifTags
import convertorlogic
from convertorlogic import convert_images_to_pdf
import subprocess



def images_to_pdf():
    if images:
        # Open a file dialog to select the location for saving the PDF file
        output_filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )

        if output_filename:
            output_file = convert_images_to_pdf(images, output_filename)



# UI Module (pdf_ui.py)
win = Tk()
win.geometry('320x540')
win.title("img.pdf")
win.attributes('-alpha', 0.95)
win.resizable(False, False)
win.iconbitmap('C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\img-pdf.ico')


images = []  # List to store selected image file paths
image_index = 0  # Index to keep track of the currently displayed

def select_files():
    global images
    images = filedialog.askopenfilenames(initialdir="", title="Select Images", filetypes=(
        ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"), ("All files", "*.*")))
    selected_files_label.config(text="\n".join(images))
    display_image(0)


def display_image(index):
    global image_index
    if 0 <= index < len(images):
        image_index = index
        image_path = images[index]
        img = Image.open(image_path)

        # Check for Exif orientation and apply it
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    exif = dict(img._getexif().items())
                    if exif[orientation] == 3:
                        img = img.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img = img.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # No Exif orientation metadata found, do nothing
            pass

        # Constant width of your application
        app_width = 320  # Replace with your actual width

        # Resize the image to match the constant width
        new_width = app_width
        new_height = int(img.height * (new_width / img.width))

        img = img.resize((new_width, new_height))

        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
        image_index_label.config(text=f"{index + 1}/{len(images)}")


def next_image():
    if images:
        new_index = (image_index + 1) % len(images)
        display_image(new_index)


def previous_image():
    if images:
        new_index = (image_index - 1) % len(images)
        display_image(new_index)


Label(win, text="img.pdf", font="Caveat 25 bold").pack(pady=10)

# SELECT BUTTON UI

button_select_inactive = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\select_images_inactive.png')
button_select_inactive_nohover = ImageTk.PhotoImage(button_select_inactive)

button_select_active = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\select_images_active.png')
button_select_active_hover = ImageTk.PhotoImage(button_select_active)

button_select_click = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\select_images_click.png')
button_select_onclick = ImageTk.PhotoImage(button_select_click)

button_select_images = Button(win, text="Select Images", image=button_select_inactive_nohover, command=select_files,
                              bd=0, relief="sunken")
button_select_images.pack(ipadx=10)


def select_on_hover(event):
    button_select_images.config(image=button_select_active_hover)


def select_on_leave(event):
    button_select_images.config(image=button_select_inactive_nohover)


def select_on_click(event):
    # Change the image or perform any action you want on button click
    button_select_images.config(image=button_select_onclick)


style = ttk.Style()
style.configure("TButton", relief="sunken")
button_select_images.bind("<Enter>", select_on_hover)
button_select_images.bind("<Leave>", select_on_leave)
button_select_images.bind("<Button-1>", select_on_click)

frame = Frame(win)
frame.pack()

# CONVERT BUTTON UI

button_convert_inactive = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\convert_inactive.png')
button_convert_inactive_nohover = ImageTk.PhotoImage(button_convert_inactive)

button_convert_active = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\convert_active.png')
button_convert_active_hover = ImageTk.PhotoImage(button_convert_active)

button_convert_click = Image.open('C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\convert_click.png')
button_convert_onclick = ImageTk.PhotoImage(button_convert_click)

button_covert = Button(frame, text="Convert and Save as PDF", image=button_convert_inactive_nohover,
                       command=images_to_pdf, bd=0, relief="sunken")
button_covert.pack(side=LEFT, pady=20, ipadx=10)


def convert_on_hover(event):
    button_covert.config(image=button_convert_active_hover)
def convert_on_leave(event):
    button_covert.config(image=button_convert_inactive_nohover)
def convert_on_click(event):
    # Change the image or perform any action you want on button click
    button_covert.config(image=button_convert_onclick)
    # win.after(200, convert_on_hover(event))

button_covert.bind("<Enter>", convert_on_hover)
button_covert.bind("<Leave>", convert_on_leave)
button_covert.bind("<Button-1>", convert_on_click)


selected_files_label = Label(win, text="", wraplength=600)

image_index_label = Label(win, text="0/0", font=("Caveat 25 bold", 20), pady=20)
image_index_label.pack()
image_label = Label(win, padx=10, pady=30)
image_label.pack()


# PREVIOUS BUTTON UI

button_previous_inactive = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\previous_inactive.png')
button_previous_inactive_nohover = ImageTk.PhotoImage(button_previous_inactive)
button_previous_active = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\previous_active.png')
button_previous_active_hover = ImageTk.PhotoImage(button_previous_active)
button_previous_click = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\previous_click.png')
button_previous_onclick = ImageTk.PhotoImage(button_previous_click)


button_previous = Button(frame, text="Previous", image=button_previous_inactive_nohover, command=previous_image, bd=0, relief="sunken")
button_previous.pack(side=LEFT)

def previous_on_hover(event):
    button_previous.config(image=button_previous_active_hover)
def previous_on_leave(event):
    button_previous.config(image=button_previous_inactive_nohover)
def previous_on_click(event):
    # Change the image or perform any action you want on button click
    button_previous.config(image=button_previous_onclick)
    # win.after(200, convert_on_hover(event))

button_previous.bind("<Enter>", previous_on_hover)
button_previous.bind("<Leave>", previous_on_leave)
button_previous.bind("<Button-1>", previous_on_click)



button_next_inactive = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\next_inactive.png')
button_next_inactive_nohover = ImageTk.PhotoImage(button_next_inactive)
button_next_active = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\next_active.png')
button_next_active_hover = ImageTk.PhotoImage(button_next_active)
button_next_click = Image.open(
    'C:\\Users\\thebo\\PycharmProjects\\imagestopdf\\design\\buttons\\next_click.png')
button_next_onclick = ImageTk.PhotoImage(button_next_click)


button_next = Button(frame, text="Next", image=button_next_inactive_nohover, command=next_image, bd=0, relief="sunken")
button_next.pack(side=LEFT, padx=10)

def next_on_hover(event):
    button_next.config(image=button_next_active_hover)
def next_on_leave(event):
    button_next.config(image=button_next_inactive_nohover)
def next_on_click(event):
    # Change the image or perform any action you want on button click
    button_next.config(image=button_next_onclick)
    # win.after(200, convert_on_hover(event))

button_next.bind("<Enter>", next_on_hover)
button_next.bind("<Leave>", next_on_leave)
button_next.bind("<Button-1>", next_on_click)


win.mainloop()
