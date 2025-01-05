import React, { useState } from 'react';
import axios from 'axios';
import '../assets/Start.css';

const Start = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [processedFiles, setProcessedFiles] = useState<Array<{ png: string, stl: string }> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isConverting, setIsConverting] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

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

  return (
    <div className="start">
      <h1>Upload Image</h1>
      <input type="file" onChange={handleFileChange} />
      {previewUrl && (
        <div className="image-preview">
          <h2>Image Preview</h2>
          <img src={previewUrl} alt="Selected" />
        </div>
      )}
      {selectedFile && (
        <div>
          <p>Selected File: {selectedFile.name}</p>
          <button onClick={handleConvert} disabled={isConverting || !selectedFile}>
            {isConverting ? 'Converting...' : 'Start Converting'}
          </button>
          <button onClick={handleCancel}>Cancel</button>
        </div>
      )}
      {processedFiles && (
        <div>
          <h2>Processed Files</h2>
          {processedFiles.map((file, index) => (
            <div key={index}>
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
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default Start;