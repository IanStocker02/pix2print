from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
from stl import mesh
import numpy as np
import os
import io
import base64

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
    brightness = np.dot(colors, [0.299, 0.587, 0.114])
    sorted_indices = np.argsort(brightness)
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
                z = layer_number * 0.1
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

def process_image(image_data, num_colors=5):
    image = Image.open(io.BytesIO(base64.b64decode(image_data.split(",")[1])))
    labels, colors = extract_key_colors(image, num_colors)
    sorted_colors, sorted_indices = sort_colors_by_brightness(colors)
    masks = create_masks_from_colors(labels, sorted_colors, sorted_indices)
    
    save_dir = "output"
    os.makedirs(save_dir, exist_ok=True)
    
    png_files = []
    stl_files = []
    for i, mask in enumerate(masks):
        hex_color = rgb_to_hex(sorted_colors[i])
        png_file = save_png_from_mask(mask, sorted_colors[i], hex_color, i, save_dir)
        stl_file = save_stl_from_mask(mask, i, save_dir)
        png_files.append(png_file)
        stl_files.append(stl_file)
    
    return png_files, stl_files