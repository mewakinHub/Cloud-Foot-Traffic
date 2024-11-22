'use client'

import React, { useEffect, useState } from 'react';
import api from '../../utils/api';

interface Config {
  username: string;
  Monitoring_status: number;
  streaming_URL: string;
  email: string | null;
}

const Configs: React.FC = () => {
  const [configs, setConfigs] = useState<Config[]>([]);
  const [editingRow, setEditingRow] = useState<string | null>(null); // Tracks the row being edited
  const [updatedURL, setUpdatedURL] = useState<string>(''); // Tracks the updated URL
  const [updatedEmail, setUpdatedEmail] = useState<string>(''); // Tracks the updated email

  useEffect(() => {
    const fetchConfigs = async () => {
      try {
        const response = await api.get<Config[]>('/configs');
        setConfigs(response.data);
      } catch (err) {
        console.error('Error fetching configs:', err);
      }
    };

    fetchConfigs();
  }, []);

  const handleEditClick = (username: string, currentURL: string, currentEmail: string | null) => {
    setEditingRow(username); // Set the row to edit mode
    setUpdatedURL(currentURL); // Set the current URL in the input field
    setUpdatedEmail(currentEmail || ''); // Set the current email in the input field
  };

  const handleSaveClick = async (username: string) => {
    try {
      // Save the updated URL
      await api.put(`/edit/${username}`, { streaming_URL: updatedURL });

      // Save the updated email
      if (updatedEmail !== '') {
        await api.put(`/email/${username}`, { email: updatedEmail });
      }

      // Update the frontend with the new URL and email
      setConfigs((prevConfigs) =>
        prevConfigs.map((config) =>
          config.username === username
            ? { ...config, streaming_URL: updatedURL, email: updatedEmail }
            : config
        )
      );
    } catch (err) {
      console.error('Error saving data:', err);
    } finally {
      setEditingRow(null); // Exit edit mode after saving
    }
  };

  return (
    <div>
      <h1>Configs Table</h1>
      <table border={1} cellPadding={10} style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            <th>Username</th>
            <th>Monitoring Status</th>
            <th>Streaming URL</th>
            <th>Email</th>
            <th>Edit</th>
          </tr>
        </thead>
        <tbody>
          {configs.map((config) => (
            <tr key={config.username}>
              <td>{config.username}</td>
              <td>{config.Monitoring_status}</td>
              <td>
                {editingRow === config.username ? (
                  <input
                    type="text"
                    value={updatedURL}
                    onChange={(e) => setUpdatedURL(e.target.value)}
                    style={{ width: '100%' }}
                  />
                ) : (
                  config.streaming_URL
                )}
              </td>
              <td>
                {editingRow === config.username ? (
                  <input
                    type="email"
                    value={updatedEmail}
                    onChange={(e) => setUpdatedEmail(e.target.value)}
                    style={{ width: '100%' }}
                  />
                ) : (
                  config.email || 'N/A'
                )}
              </td>
              <td>
                {editingRow === config.username ? (
                  <button onClick={() => handleSaveClick(config.username)}>Save</button>
                ) : (
                  <button onClick={() => handleEditClick(config.username, config.streaming_URL, config.email || '')}>
                    Edit
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Configs;