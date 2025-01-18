import os
from PIL import Image

def imgcrop(input, xPieces, yPieces):
    filename, file_extension = os.path.splitext(input)
    im = Image.open(input)
    imgwidth, imgheight = im.size
    height = imgheight // yPieces
    width = imgwidth // xPieces
    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            a = im.crop(box)
            try:
                a.save("img/" + filename + "-" + str(i) + "-" + str(j) + file_extension)
            except:
                pass

if __name__ == "__main__":
    imgcrop("test_image.jpg", 4, 2)
