import os
from PIL import Image, ImageDraw
import numpy as np
from sklearn.cluster import KMeans
from stl import mesh
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload and processed directories
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

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
    sorted_indices = np.argsort(brightness)  # Darkest to lightest
    return colors[sorted_indices], sorted_indices

def create_masks_from_colors(labels, colors, sorted_indices):
    masks = []
    for i in sorted_indices:
        mask = np.where(labels == i, 255, 0).astype(np.uint8)
        masks.append(mask)
    return masks

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

@app.route('/process-image', methods=['POST'])
def process_image_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.png'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            processed_message = process_image(file_path, app.config['PROCESSED_FOLDER'])
            # Return the path to the processed file
            return jsonify({'processedFilePath': processed_message}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 400

def process_image(image_path, save_dir, num_colors=5):
    image = Image.open(image_path)
    labels, colors = extract_key_colors(image, num_colors)
    colors, sorted_indices = sort_colors_by_brightness(colors)
    masks = create_masks_from_colors(labels, colors, sorted_indices)

    processed_files = []

    for idx, (mask, color) in enumerate(zip(masks, colors)):
        hex_color = f"{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        layer_number = len(colors) - idx
        png_file = save_png_from_mask(mask, color, hex_color, layer_number, save_dir)
        stl_file = save_stl_from_mask(mask, layer_number, save_dir)
        
        processed_files.append({'png': png_file, 'stl': stl_file})

    return f"Processed image saved to {save_dir}. Files: {processed_files}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)