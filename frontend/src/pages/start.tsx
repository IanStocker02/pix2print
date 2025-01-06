import React, { useState } from 'react';
import axios from 'axios';
import '../assets/Start.css';

const Start = () => {
  // State Variables
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [processedFiles, setProcessedFiles] = useState<Array<{ png: string; stl: string }> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isConverting, setIsConverting] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [numLayers, setNumLayers] = useState<number>(5);
  const [quality, setQuality] = useState<string>('low');

  // Handlers
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const file = event.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleConvert = async () => {
    if (!selectedFile) return;

    setIsConverting(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('num_layers', numLayers.toString());
    formData.append('quality', quality);

    try {
      const response = await axios.post('http://localhost:5000/images/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setProcessedFiles(response.data.files);
      setError(null);
    } catch (error) {
      console.error('Upload failed:', error);
      setError('Upload failed. Please try again.');
    } finally {
      setIsConverting(false);
    }
  };

  const handleCancel = () => {
    setSelectedFile(null);
    setProcessedFiles(null);
    setPreviewUrl(null);
    setError(null);
  };

  // Render
  return (
    <div className="start">
      <h1>Upload Image</h1>
      <input type="file" onChange={handleFileChange} />

      {previewUrl && (
        <div className="image-preview">
          <h2>Image Preview</h2>
          <img src={previewUrl} alt="Selected Preview" />
        </div>
      )}

      {selectedFile && (
        <div className="settings">
          <p>
            <strong>Selected File:</strong> {selectedFile.name}
          </p>

          <div className="setting-group">
            <label>
              Number of Layers:
              <span className="tooltip">
                ℹ️
                <span className="tooltip-text">Adjust the number of image layers.</span>
              </span>
              <input
                type="range"
                min="2"
                max="10"
                value={numLayers}
                onChange={(e) => setNumLayers(parseInt(e.target.value))}
              />
              <span>{numLayers}</span>
            </label>
          </div>

          <div className="setting-group">
            <label>
              Quality:
              <span className="tooltip">
                ℹ️
                <span className="tooltip-text">Select the quality level for conversion.</span>
              </span>
              <select value={quality} onChange={(e) => setQuality(e.target.value)}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </label>
          </div>

          <div className="actions">
            <button onClick={handleConvert} disabled={isConverting || !selectedFile}>
              {isConverting ? 'Converting...' : 'Start Converting'}
            </button>
            <button onClick={handleCancel}>Cancel</button>
          </div>
        </div>
      )}

      {processedFiles && (
        <div className="processed-files">
          <h2>Processed Files</h2>
          {processedFiles.map((file, index) => (
            <div key={index} className="file-links">
              <a href={`http://localhost:5000/images/download/${file.png}`} download>
                Download PNG Layer {index + 1}
              </a>
              <a href={`http://localhost:5000/images/download/${file.stl}`} download>
                Download STL Layer {index + 1}
              </a>
            </div>
          ))}
        </div>
      )}

      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default Start;
