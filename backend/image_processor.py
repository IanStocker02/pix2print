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
    labels = kmeans.labels_
    return labels.reshape(image.size[1], image.size[0]), colors

def sort_colors_by_brightness(colors):
    brightness = np.sum(colors, axis=1)
    sorted_indices = np.argsort(brightness)
    sorted_colors = colors[sorted_indices]
    return sorted_colors, sorted_indices

def create_masks_from_colors(labels, colors, sorted_indices):
    h, w = labels.shape
    masks = []
    for color_idx in sorted_indices:
        mask = np.zeros((h, w), dtype=np.uint8)
        mask[labels == color_idx] = 255
        masks.append(mask)
    return masks

def save_png_from_mask(mask, color, hex_color, layer_number, save_dir):
    filename = f"layer_{layer_number}.png"
    filepath = os.path.join(save_dir, filename)
    image = Image.fromarray(mask)
    image.save(filepath)
    return filename

def save_stl_from_mask(mask, layer_number, save_dir):
    filename = f"layer_{layer_number}.stl"
    filepath = os.path.join(save_dir, filename)
    
    # Ensure mask is a NumPy array
    if not isinstance(mask, np.ndarray):
        raise ValueError("mask should be a NumPy array")
    
    h, w = mask.shape[:2]
    vertices = []
    vertex_indices = -np.ones((h, w), dtype=int)

    # Create vertices and vertex indices
    for y in range(h):
        for x in range(w):
            if mask[y, x] > 0:  # Assuming mask is a binary mask
                vertex_indices[y, x] = len(vertices)
                vertices.append([x, y, 0])

    vertices = np.array(vertices)
    faces = []

    # Create faces
    for y in range(1, h):
        for x in range(1, w):
            if mask[y, x] > 0:
                if vertex_indices[y, x] != -1 and vertex_indices[y, x - 1] != -1 and vertex_indices[y - 1, x] != -1:
                    faces.append([vertex_indices[y, x], vertex_indices[y, x - 1], vertex_indices[y - 1, x]])
                if vertex_indices[y - 1, x] != -1 and vertex_indices[y, x - 1] != -1 and vertex_indices[y - 1, x - 1] != -1:
                    faces.append([vertex_indices[y - 1, x], vertex_indices[y, x - 1], vertex_indices[y - 1, x - 1]])

    faces = np.array(faces)

    # Create the mesh
    stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            stl_mesh.vectors[i][j] = vertices[f[j], :]

    stl_mesh.save(filepath)
    return filename

def process_image(input_path, output_folder, num_colors=5):
    image = Image.open(input_path)
    labels, colors = extract_key_colors(image, num_colors)
    colors, sorted_indices = sort_colors_by_brightness(colors)
    masks = create_masks_from_colors(labels, colors, sorted_indices)
    processed_files = []

    for idx, (mask, color) in enumerate(zip(masks, colors)):
        hex_color = f"{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}"
        layer_number = len(colors) - idx
        png_file = save_png_from_mask(mask, color, hex_color, layer_number, output_folder)
        stl_file = save_stl_from_mask(mask, layer_number, output_folder)
        processed_files.append({'png': png_file, 'stl': stl_file})

    return processed_files