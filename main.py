import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image as RLImage
import os

class ImageToPdfConverter:
    def _init_(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")

        # Create GUI elements
        self.label = tk.Label(root, text="Select Image(s):")
        self.label.pack()

        self.add_button = tk.Button(root, text="Add Images", command=self.add_images)
        self.add_button.pack()

        self.image_paths = []
        self.image_previews = []

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.convert_button = tk.Button(root, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_button.pack()

    def add_images(self):
        self.image_paths = filedialog.askopenfilenames(
            title="Select Image(s)",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )

        # Display image previews
        for path in self.image_paths:
            img = Image.open(path)
            img.thumbnail((100, 100))
            img = ImageTk.PhotoImage(img)
            self.image_previews.append(img)
            label = tk.Label(self.root, image=img)
            label.image = img
            label.pack()

    def convert_to_pdf(self):
        if not self.image_paths:
            print("No images selected for conversion.")
            return

        pdf_filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not pdf_filename:
            return

        try:
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            elements = []

            for image_path in self.image_paths:
                try:
                    img = Image.open(image_path)
                    width, height = img.size
                    img.thumbnail((400, 400))
                    img_path = "temp_img.jpg"  # Temporary image file
                    img.save(img_path)

                    rl_img = RLImage(img_path, width=width, height=height)
                    elements.append(rl_img)
                except Exception as e:
                    print(f"Error converting {os.path.basename(image_path)}: {str(e)}")

            if elements:
                doc.build(elements)
                print(f"PDF saved as {pdf_filename}")
            else:
                print("No valid images to convert.")

        except Exception as e:
            print(f"Error creating PDF: {str(e)}")

if _name_ == "_main_":
    root = tk.Tk()
    app = ImageToPdfConverter(root)
    root.mainloop()