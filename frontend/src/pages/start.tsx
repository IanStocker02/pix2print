import React, { useState } from 'react';
import axios from 'axios';
import '../assets/Start.css';

const Start = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [processedFilePath, setProcessedFilePath] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      if (file.type === 'image/png') {
        setSelectedFile(file);
        const url = URL.createObjectURL(file);
        setPreviewUrl(url);
      } else {
        setError('Please upload a valid .png file.');
        setSelectedFile(null);
        setPreviewUrl(null);
      }
    }
  };

  const handleCancel = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setError(null);
    setProcessedFilePath(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/images/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setProcessedFilePath(response.data.file_path);
      setError(null);
    } catch (error) {
      console.error('Upload failed:', error);
      setError('Upload failed. Please try again.');
    }
  };

  return (
    <div className="start">
      <h1>Upload Image</h1>
      <input type="file" accept=".png" onChange={handleFileChange} />
      {error && <p className="error">{error}</p>}
      {previewUrl && (
        <div className="image-preview">
          <h2>Image Preview</h2>
          <img src={previewUrl} alt="Selected" />
        </div>
      )}
      {selectedFile && (
        <div>
          <p>Selected File: {selectedFile.name}</p>
          <button onClick={handleUpload} disabled={!selectedFile}>
            Upload
          </button>
          <button onClick={handleCancel}>Cancel</button>
        </div>
      )}
      {processedFilePath && (
        <div>
          <h2>Processed Image</h2>
          <a href={`http://localhost:8000/images/download/${processedFilePath}`} download>
            Download Processed Image
          </a>
        </div>
      )}
    </div>
  );
};

export default Start;
