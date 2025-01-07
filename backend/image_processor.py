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

def rgb_to_hex(rgb):
    return '{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def save_png_from_mask(mask, color, hex_color, layer_number, save_dir):
    h, w = mask.shape
    colored_image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(colored_image)
    for y in range(h):
        for x in range(w):
            if mask[y, x] == 255:
                draw.point((x, y), fill=(int(color[0]), int(color[1]), int(color[2]), 255))

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

def process_image(input_path, output_folder, num_colors=5):
    image = Image.open(input_path)
    labels, colors = extract_key_colors(image, num_colors)
    colors, sorted_indices = sort_colors_by_brightness(colors)
    masks = create_masks_from_colors(labels, colors, sorted_indices)
    processed_files = []

    cumulative_mask = np.zeros_like(masks[0], dtype=np.uint8)
    total_layers = len(colors)

    for idx, (mask, color) in enumerate(zip(masks, colors)):
        hex_color = rgb_to_hex(color)
        layer_number = total_layers - idx
        mask = np.maximum(mask, cumulative_mask)
        cumulative_mask = np.maximum(cumulative_mask, mask)
        png_file = save_png_from_mask(cumulative_mask, color, hex_color, layer_number, output_folder)
        stl_file = save_stl_from_mask(cumulative_mask, layer_number, output_folder)
        
        # Debug statements to check file paths
        print(f"Saved PNG file: {png_file}")
        print(f"Saved STL file: {stl_file}")
        
        processed_files.append({'png': png_file, 'stl': stl_file})

    return processed_files