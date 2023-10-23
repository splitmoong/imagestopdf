import img2pdf

import img2pdf


def convert_images_to_pdf(image_paths, output_filename):
    if image_paths:
        with open(output_filename, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert(image_paths))
        return output_filename
    return None
