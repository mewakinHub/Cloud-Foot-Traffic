'use client';

import React, { useState } from 'react';
import api from '../../utils/api';

const GetData: React.FC = () => {
  const [username, setUsername] = useState('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleDownload = async () => {
    try {
      // Clear any previous error message
      setErrorMessage(null);

      // Make the API call to download the file
      const response = await api.get(`/download_image/${username}`, {
        responseType: 'blob', // Important for file downloads
      });

      // Create a temporary URL for the file and trigger the download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${username}_image.zip`); // Default filename
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error: any) {
      // Check if the error is due to a non-existent username
      if (error.response && error.response.status === 404) {
        setErrorMessage('Username does not exist or does not have any image.');
      } else {
        setErrorMessage('An error occurred while processing the request.');
      }
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Download Image</h1>
      <div>
        <input
          type="text"
          placeholder="Enter username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{
            padding: '10px',
            fontSize: '16px',
            marginRight: '10px',
            width: '300px',
          }}
        />
        <button
          onClick={handleDownload}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            cursor: 'pointer',
          }}
        >
          Download
        </button>
      </div>
      {errorMessage && (
        <div
          style={{
            marginTop: '20px',
            color: 'red',
            fontWeight: 'bold',
          }}
        >
          {errorMessage}
        </div>
      )}
    </div>
  );
};

export default GetData;
