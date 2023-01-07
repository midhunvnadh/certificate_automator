import pandas as pd
import os
import cv2
from PIL import Image, ImageDraw, ImageFont

"""Settings"""
fonts_dir = 'fonts'
font_name = "NotoSans-Black"
certificate_dir = 'certificate'
csv_file = "data.csv"
csv_handle = ["First Name", "Last Name"]
placement = {
    "x": 450,
    "y": 580,
    "height": 55,
    "width": 790,
    "fontSize": 55
}
"""Settings End"""

df = pd.read_csv(csv_file, usecols=csv_handle)

def names():
    texts = []
    for index, row in df.iterrows():
        text = ""
        for handle in csv_handle:
            text += row[handle].replace("."," ").strip() + " "
        text = text.replace("  ", " ").upper().strip()
        texts.append(text)
    return(texts)

def get_certificate_from_dir():
    certificate = []
    for file in os.listdir(certificate_dir):
        if file.endswith(".jpg"):
            certificate.append(file)
    return(certificate[0])

def get_certificate(filename):
    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    return(img.shape[0], img.shape[1], filename)

def new_pil_image(width, height):
    return(Image.new('RGBA', (width, height), (255, 255, 255, 0)))

def draw_text_on_image(image, text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(f"{fonts_dir}/{font_name}.ttf", placement["fontSize"])
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    x = placement["x"] + (placement["width"] - w) / 2
    y = placement["y"]
    draw.text((x, y), text, (0, 0, 0), font=font)
    return(image)

def merge_images(image, certificate):
    certificate = Image.open(certificate)
    certificate.paste(image, (0,0), image)
    return(certificate)

def main():
    all_names = names()
    certificate = get_certificate_from_dir()
    height, width, path = get_certificate(certificate_dir + "/" + certificate)
    for name in all_names:
        image = new_pil_image(width, height)
        image = draw_text_on_image(image, name)
        image = merge_images(image,path)
        image.save(f"generated/{name}.jpg")
        print(f"Generated {name}.jpg")
if __name__ == "__main__":
    main()