import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2 as cv
from PIL import Image, ImageTk
import numpy as np
import multiprocessing


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        # Główne kontenery
        self.menu_frame = tk.Frame(root, width=200, bg="lightgray")
        self.menu_frame.pack(side="left", fill="y")

        self.image_frame = tk.Frame(root, bg="white")
        self.image_frame.pack(side="right", expand=True, fill="both")

        # Elementy menu
        ttk.Label(self.menu_frame, text="Opcje", font=("Arial", 14)).pack(pady=10)

        self.open_button = ttk.Button(self.menu_frame, text="Otwórz obraz", command=self.open_image)
        self.open_button.pack(fill="x", padx=10, pady=5)

        self.gray_button = ttk.Button(self.menu_frame, text="Konwertuj na szarość", command=self.apply_grayscale)
        self.gray_button.pack(fill="x", padx=10, pady=5)

        self.invert_button = ttk.Button(self.menu_frame, text="Negatyw", command=self.apply_inversion)
        self.invert_button.pack(fill="x", padx=10, pady=5)

        self.saturation_scale = tk.Scale(self.menu_frame, from_=0, to=200, orient="horizontal", label="Nasycenie")
        self.saturation_scale.set(100)
        self.saturation_scale.pack(fill="x", padx=10, pady=5)

        self.apply_saturation_button = ttk.Button(self.menu_frame, text="Zastosuj nasycenie",
                                                  command=self.apply_saturation)
        self.apply_saturation_button.pack(fill="x", padx=10, pady=5)

        self.reset_button = ttk.Button(self.menu_frame, text="Resetuj obraz", command=self.reset_image)
        self.reset_button.pack(fill="x", padx=10, pady=5)

        self.save_button = ttk.Button(self.menu_frame, text="Zapisz obraz", command=self.save_image)
        self.save_button.pack(fill="x", padx=10, pady=5)

        self.quit_button = ttk.Button(self.menu_frame, text="Zamknij", command=root.quit)
        self.quit_button.pack(fill="x", padx=10, pady=5)

        # Element wyświetlania obrazu
        self.image_label = tk.Label(self.image_frame, text="Brak wczytanego obrazu", bg="white")
        self.image_label.pack(expand=True)

        self.image = None
        self.processed_image = None
        self.use_multiprocessing = tk.BooleanVar()

        self.multiprocessing_checkbox = tk.Checkbutton(self.menu_frame, text="Włącz multiprocessing",
                                                       variable=self.use_multiprocessing)
        self.multiprocessing_checkbox.pack(fill="x", padx=10, pady=5)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")])
        if file_path:
            self.image = cv.imread(file_path)
            self.processed_image = None
            self.show_image(self.image)

    def show_image(self, image):
        # Convert BGR to RGB and display
        rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        tk_image = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=tk_image, text="")
        self.image_label.image = tk_image  # Keep a reference

    def apply_grayscale(self):
        if self.image is not None:
            base_image = self.processed_image if self.processed_image is not None else self.image
            self.processed_image = cv.cvtColor(base_image, cv.COLOR_BGR2GRAY)
            self.show_image(cv.cvtColor(self.processed_image, cv.COLOR_GRAY2BGR))

    def apply_inversion(self):
        if self.image is not None:
            base_image = self.processed_image if self.processed_image is not None else self.image
            self.processed_image = 255 - base_image
            self.show_image(self.processed_image)

    def apply_saturation(self):
        if self.image is not None:
            base_image = self.processed_image if self.processed_image is not None else self.image
            saturation_factor = self.saturation_scale.get() / 100
            hsv_image = cv.cvtColor(base_image, cv.COLOR_BGR2HSV).astype(np.float32)
            hsv_image[..., 1] *= saturation_factor
            hsv_image[..., 1] = np.clip(hsv_image[..., 1], 0, 255)
            self.processed_image = cv.cvtColor(hsv_image.astype(np.uint8), cv.COLOR_HSV2BGR)
            self.show_image(self.processed_image)

    def reset_image(self):
        if self.image is not None:
            self.processed_image = None
            self.show_image(self.image)

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if file_path:
                cv.imwrite(file_path, self.processed_image)

    def process_tile(self, tile):
        """Przetwarzanie pojedynczego fragmentu obrazu."""
        # Negatyw
        tile = 255 - tile

        # Szarość - przekształć na odcienie szarości
        gray_tile = cv.cvtColor(tile, cv.COLOR_BGR2GRAY)

        # Jeśli obraz jest w odcieniach szarości (ma tylko jeden kanał), przywróć trzy kanały
        if len(gray_tile.shape) == 2:  # Tylko jeden kanał (szarość)
            gray_tile = cv.cvtColor(gray_tile, cv.COLOR_GRAY2BGR)  # Przywracamy 3 kanały (BGR)

        # Nasycenie - przechodzimy do przestrzeni HSV
        hsv_image = cv.cvtColor(gray_tile, cv.COLOR_BGR2HSV).astype(np.float32)
        saturation_factor = self.saturation_scale.get() / 100
        hsv_image[..., 1] *= saturation_factor  # Zastosowanie nasycenia
        hsv_image[..., 1] = np.clip(hsv_image[..., 1], 0, 255)

        # Z powrotem do przestrzeni BGR
        tile = cv.cvtColor(hsv_image.astype(np.uint8), cv.COLOR_HSV2BGR)

        return tile

    def apply_all_processing(self):
        if self.image is not None:
            num_processes = 4  # Przykład, 4 procesy
            height, width = self.image.shape[:2]
            strips = []

            # Dzielimy obraz na pasy
            for i in range(num_processes):
                strip_height = height // num_processes
                start_y = i * strip_height
                end_y = (i + 1) * strip_height if i != num_processes - 1 else height
                strips.append(self.image[start_y:end_y, :])

            # Jeśli użytkownik zaznaczył multiprocessing, używamy go
            if self.use_multiprocessing.get():
                pool = multiprocessing.Pool(num_processes)
                processed_strips = pool.map(self.process_tile, strips)
                pool.close()
                pool.join()

                # Łączymy z powrotem przetworzone paski
                self.processed_image = np.vstack(processed_strips)
            else:
                # Bez multiprocessing - przetwarzamy po kolei
                self.processed_image = np.vstack([self.process_tile(strip) for strip in strips])

            self.show_image(self.processed_image)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = ImageProcessorApp(root)
    root.mainloop()
