import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import numpy as np
from sklearn.cluster import KMeans
from stl import mesh
import os


def extract_key_colors(image, num_colors=5):
    image_np = np.array(image.convert("RGB"))
    h, w, _ = image_np.shape
    pixels = image_np.reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_.reshape(h, w)
    return labels, colors


def create_masks_from_colors(labels, colors):
    masks = []
    for i in range(len(colors)):
        mask = np.where(labels == i, 255, 0).astype(np.uint8)
        masks.append(mask)
    return masks


def rgb_to_hex(rgb):
    return '{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def generate_stl_from_mask(mask, layer_height=1):
    h, w = mask.shape
    vertices = []
    faces = []

    for y in range(h):
        for x in range(w):
            if mask[y, x] == 255:
                vertices.append([x, y, 0])
                vertices.append([x, y, layer_height])

    if len(vertices) < 3:
        return None

    vertices = np.array(vertices)
    for i in range(0, len(vertices) - 2, 2):
        faces.append([i, i + 1, i + 2])

    mesh_data = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for j, f in enumerate(faces):
        for k in range(3):
            mesh_data.vectors[j][k] = vertices[f[k], :]

    return mesh_data


def save_png_from_mask(mask, color, hex_color, layer_number, save_dir):
    h, w = mask.shape
    colored_image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(colored_image)
    for y in range(h):
        for x in range(w):
            if mask[y, x] == 255:
                draw.point((x, y), fill=(color[0], color[1], color[2], 255))

    png_filename = os.path.join(save_dir, f"{hex_color}_{layer_number}.png")
    colored_image.save(png_filename)
    return png_filename


class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to STL Converter")
        self.root.geometry("700x800")
        self.root.configure(bg='#2c2c2c')
        self.save_dir = os.getcwd()

        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=6, relief="flat", background="#4caf50")
        self.style.configure("TLabel", background="#2c2c2c", foreground="#ffffff")
        self.style.configure("TFrame", background="#2c2c2c")

        # Frames for better organization
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(pady=10)

        self.mid_frame = ttk.Frame(root)
        self.mid_frame.pack(pady=10)

        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(pady=20)

        # Widgets
        self.upload_btn = ttk.Button(self.top_frame, text="Upload Photo", command=self.upload_photo)
        self.upload_btn.grid(row=0, column=0, padx=5)

        self.save_dir_btn = ttk.Button(self.top_frame, text="Select Save Location", command=self.select_save_directory)
        self.save_dir_btn.grid(row=0, column=1, padx=5)

        self.convert_btn = ttk.Button(self.top_frame, text="Convert to STL", command=self.convert_photo)
        self.convert_btn.grid(row=0, column=2, padx=5)

        # Number of Colors Label, Slider, and Value Display
        self.num_colors_label = ttk.Label(self.mid_frame, text="Number of Colors:")
        self.num_colors_label.grid(row=0, column=0, padx=5)

        self.num_colors_value = ttk.Label(self.mid_frame, text="5")
        self.num_colors_value.grid(row=0, column=2, padx=5)

        self.num_colors_slider = ttk.Scale(
            self.mid_frame, from_=2, to=10, orient='horizontal',
            command=self.update_color_value
        )
        self.num_colors_slider.set(5)
        self.num_colors_slider.grid(row=0, column=1, padx=5)

        self.progress = ttk.Progressbar(self.mid_frame, orient='horizontal', length=400, mode='determinate')
        self.progress.grid(row=1, columnspan=3, pady=10)

        self.image_label = ttk.Label(self.bottom_frame)
        self.image_label.pack(pady=5)

        self.console_log = tk.Text(self.bottom_frame, height=10, width=80, bg="#1e1e1e", fg="#ffffff", state="disabled")
        self.console_log.pack(pady=10)

        self.image = None

    def update_color_value(self, value):
        """Update the displayed number of colors based on slider value."""
        self.num_colors_value.config(text=str(int(float(value))))

    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)
            self.log_console("Image uploaded successfully.")

    def select_save_directory(self):
        self.save_dir = filedialog.askdirectory()
        self.log_console(f"Selected Save Location: {self.save_dir}")

    def convert_photo(self):
        if not self.image:
            self.log_console("No image uploaded.")
            return

        num_colors = int(self.num_colors_slider.get())
        labels, colors = extract_key_colors(self.image, num_colors)
        self.log_console(f"Extracted Colors: {colors.tolist()}")

        masks = create_masks_from_colors(labels, colors)
        cumulative_mask = np.zeros_like(masks[0], dtype=np.uint8)
        base_mask = np.full_like(masks[0], 255)

        self.progress['maximum'] = len(colors) + 1
        self.progress['value'] = 0

        save_png_from_mask(base_mask, (255, 255, 255), "ffffff", 0, self.save_dir)
        cumulative_mask = np.maximum(cumulative_mask, base_mask)

        for idx, (mask, color) in enumerate(zip(masks, colors)):
            hex_color = rgb_to_hex(color)
            layer_number = idx + 1
            filtered_mask = np.where((mask == 255) & (cumulative_mask == 255), 255, 0)

            if np.count_nonzero(filtered_mask) == 0:
                self.log_console(f"Skipping layer {layer_number}.")
                continue

            save_png_from_mask(filtered_mask, color, hex_color, layer_number, self.save_dir)
            cumulative_mask = np.maximum(cumulative_mask, filtered_mask)

            self.progress['value'] += 1
            self.root.update_idletasks()

        self.log_console("Conversion Completed!")
        self.progress['value'] = len(colors) + 1

    def display_image(self, image):
        image.thumbnail((400, 400))
        tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image

    def log_console(self, message):
        self.console_log.config(state="normal")
        self.console_log.insert(tk.END, message + "\n")
        self.console_log.config(state="disabled")
        self.console_log.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()