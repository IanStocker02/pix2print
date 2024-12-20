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


def sort_colors_by_brightness(colors):
    # Calculate brightness using a weighted sum (perceived brightness formula)
    brightness = np.dot(colors, [0.299, 0.587, 0.114])
    sorted_indices = np.argsort(brightness)  # Darkest to lightest
    return colors[sorted_indices], sorted_indices


def create_masks_from_colors(labels, colors, sorted_indices):
    masks = []
    for i in sorted_indices:
        mask = np.where(labels == i, 255, 0).astype(np.uint8)
        masks.append(mask)
    return masks


def rgb_to_hex(rgb):
    return '{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


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

def save_stl_from_mask(mask, layer_number, save_dir):
    h, w = mask.shape
    vertices = []
    faces = []

    for y in range(h):
        for x in range(w):
            if mask[y, x] == 255:
                # Add vertices for a square at each pixel
                z = layer_number * 0.1  # Adjust height for each layer
                v0 = [x, y, z]
                v1 = [x + 1, y, z]
                v2 = [x + 1, y + 1, z]
                v3 = [x, y + 1, z]
                vertices.extend([v0, v1, v2, v3])
                base_idx = len(vertices) - 4
                faces.append([base_idx, base_idx + 1, base_idx + 2])
                faces.append([base_idx, base_idx + 2, base_idx + 3])

    vertices = np.array(vertices)
    faces = np.array(faces)
    if len(faces) > 0:
        stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                stl_mesh.vectors[i][j] = vertices[f[j], :]

        stl_filename = os.path.join(save_dir, f"layer_{layer_number}.stl")
        stl_mesh.save(stl_filename)
        return stl_filename
    return None

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

        # Resolution Dropdown
        self.resolution_label = ttk.Label(self.mid_frame, text="Resolution:")
        self.resolution_label.grid(row=1, column=0, padx=5)

        self.resolution_var = tk.StringVar(value="Low")
        self.resolution_dropdown = ttk.Combobox(self.mid_frame, textvariable=self.resolution_var, values=["Low", "Medium", "High"])
        self.resolution_dropdown.grid(row=1, column=1, padx=5)

        self.progress = ttk.Progressbar(self.mid_frame, orient='horizontal', length=400, mode='determinate')
        self.progress.grid(row=2, columnspan=3, pady=10)

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
        resolution = self.resolution_var.get()

        # Adjust image resolution based on the selected option
        if resolution == "High":
            scale_factor = 4
        elif resolution == "Medium":
            scale_factor = 2
        else:
            scale_factor = 1

        new_size = (self.image.width * scale_factor, self.image.height * scale_factor)
        high_res_image = self.image.resize(new_size, Image.LANCZOS)

        labels, colors = extract_key_colors(high_res_image, num_colors)

        # Sort colors by brightness (darkest to lightest)
        colors, sorted_indices = sort_colors_by_brightness(colors)
        self.log_console(f"Sorted Colors: {colors.tolist()}")

        masks = create_masks_from_colors(labels, colors, sorted_indices)

        # Initialize a cumulative mask with the same shape as individual masks
        cumulative_mask = np.zeros_like(masks[0], dtype=np.uint8)

        self.progress['maximum'] = len(colors) + 1
        self.progress['value'] = 0

        total_layers = len(colors)  # Get the total number of layers

        for idx, (mask, color) in enumerate(zip(masks, colors)):
            hex_color = rgb_to_hex(color)

            # Assign layer numbers in reverse order
            layer_number = total_layers - idx

            # Fill in any pixels from previous layers if they overlap in the current mask
            mask = np.maximum(mask, cumulative_mask)

            # Update the cumulative mask to include the current layer
            cumulative_mask = np.maximum(cumulative_mask, mask)

            # Save PNG and STL using the updated cumulative mask
            save_png_from_mask(cumulative_mask, color, hex_color, layer_number, self.save_dir)
            save_stl_from_mask(cumulative_mask, layer_number, self.save_dir)

            self.progress['value'] += 1
            self.root.update_idletasks()

        self.log_console("Conversion Completed with Reversed Layer Order!")
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