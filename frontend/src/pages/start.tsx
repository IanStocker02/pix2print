import React, { useState } from 'react';
import axios from 'axios';
import '../assets/Start.css';

const Start = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [processedFilePath, setProcessedFilePath] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
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
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {error && <p className="error">{error}</p>}
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