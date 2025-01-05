import os
from PIL import Image, ImageDraw
import numpy as np
from sklearn.cluster import KMeans
from stl import mesh

def extract_key_colors(image, num_colors=5):
    image = image.convert('RGB')
    np_image = np.array(image)
    np_image = np_image.reshape((np_image.shape[0] * np_image.shape[1], 3))
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(np_image)
    colors = kmeans.cluster_centers_
    return colors

def save_png_from_mask(mask, color, hex_color, layer_number, save_dir):
    filename = f"layer_{layer_number}.png"
    filepath = os.path.join(save_dir, filename)
    image = Image.fromarray(mask)
    image.save(filepath)
    return filename

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

def process_image(input_path, output_folder, num_layers=5, quality='low'):
    image = Image.open(input_path)
    
    if quality == 'high':
        image = image.resize((image.width * 4, image.height * 4), Image.LANCZOS)
    elif quality == 'medium':
        image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
    
    colors = extract_key_colors(image, num_layers)
    masks = [np.array(image)] * len(colors)
    processed_files = []

    for idx, (mask, color) in enumerate(zip(masks, colors)):
        hex_color = f"{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}"
        layer_number = idx + 1
        png_file = save_png_from_mask(mask, color, hex_color, layer_number, output_folder)
        stl_file = save_stl_from_mask(mask, layer_number, output_folder)
        processed_files.append({'png': png_file, 'stl': stl_file})

    return processed_files