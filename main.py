import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2 as cv
from PIL import Image, ImageTk
import numpy as np


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        # UI elements
        self.image_label = tk.Label(root, text="No image loaded")
        self.image_label.pack()

        self.open_button = ttk.Button(root, text="Open Image", command=self.open_image)
        self.open_button.pack()

        self.gray_button = ttk.Button(root, text="Convert to Grayscale", command=self.apply_grayscale)
        self.gray_button.pack()

        self.invert_button = ttk.Button(root, text="Invert Colors", command=self.apply_inversion)
        self.invert_button.pack()

        self.saturation_scale = tk.Scale(root, from_=0, to=200, orient="horizontal", label="Saturation")
        self.saturation_scale.set(100)
        self.saturation_scale.pack()

        self.apply_saturation_button = ttk.Button(root, text="Apply Saturation", command=self.apply_saturation)
        self.apply_saturation_button.pack()

        self.save_button = ttk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.image = None
        self.processed_image = None

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.image = cv.imread(file_path)
            self.show_image(self.image)

    def show_image(self, image):
        # Convert BGR to RGB and display
        rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        tk_image = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image  # Keep a reference

    def apply_grayscale(self):
        if self.image is not None:
            self.processed_image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
            self.show_image(cv.cvtColor(self.processed_image, cv.COLOR_GRAY2BGR))

    def apply_inversion(self):
        if self.image is not None:
            self.processed_image = 255 - self.image
            self.show_image(self.processed_image)

    def apply_saturation(self):
        if self.image is not None:
            saturation_factor = self.saturation_scale.get() / 100
            hsv_image = cv.cvtColor(self.image, cv.COLOR_BGR2HSV).astype(np.float32)
            hsv_image[..., 1] *= saturation_factor
            hsv_image[..., 1] = np.clip(hsv_image[..., 1], 0, 255)
            self.processed_image = cv.cvtColor(hsv_image.astype(np.uint8), cv.COLOR_HSV2BGR)
            self.show_image(self.processed_image)

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                cv.imwrite(file_path, self.processed_image)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
