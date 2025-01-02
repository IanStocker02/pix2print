import React, { useState } from 'react';
import axios from 'axios';
import '../assets/Start.css';

const Start = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [processedFiles, setProcessedFiles] = useState<string[]>([]);
  const [numLayers, setNumLayers] = useState<number>(5);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
      console.log('File selected:', event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/images/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const { filename } = response.data;
      setProcessedFiles([filename]);  // Update this to handle multiple files if needed
      setError(null);
      console.log('Upload successful:', response.data);
    } catch (error) {
      console.error('Upload failed:', error);
      setError('Upload failed. Please try again.');
    }
  };

  const handleConvert = async () => {
    if (!selectedFile) return;

    try {
      const response = await axios.post('http://localhost:5000/images/convert', {
        filename: selectedFile.name,
        numLayers: numLayers,
      });
      const { processedFiles } = response.data;
      setProcessedFiles(processedFiles);
      setError(null);
      console.log('Conversion successful:', response.data);
    } catch (error) {
      console.error('Conversion failed:', error);
      setError('Conversion failed. Please try again.');
    }
  };

  const handleDownloadAll = () => {
    processedFiles.forEach((file) => {
      window.location.href = `http://localhost:5000/images/download/${file}`;
    });
    console.log('Download all files:', processedFiles);
  };

  return (
    <div className="start">
      <h1>Upload Image</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {selectedFile && (
        <div>
          <h2>Selected Image</h2>
          <img src={URL.createObjectURL(selectedFile)} alt="Selected" style={{ maxWidth: '100%' }} />
        </div>
      )}
      <div>
        <label htmlFor="numLayers">Number of Layers: {numLayers}</label>
        <input
          type="range"
          id="numLayers"
          min="1"
          max="10"
          value={numLayers}
          onChange={(e) => setNumLayers(Number(e.target.value))}
        />
      </div>
      <button onClick={handleConvert}>Convert</button>
      {error && <p className="error">{error}</p>}
      {processedFiles.length > 0 && (
        <div>
          <h2>Processed Files</h2>
          {processedFiles.map((file, index) => (
            <div key={index}>
              <button onClick={() => handleDownloadAll()}>Download All Files</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Start;