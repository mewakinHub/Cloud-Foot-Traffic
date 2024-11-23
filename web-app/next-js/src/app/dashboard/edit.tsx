'use client';

import React, { useState } from "react";
import api from '../../utils/api'; // Adjust the import path if needed

export default function Edit({ username }) {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    streaming_URL: '',
    email: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSave = async () => {
    try {
      const response = await api.put(`/update/config/${username}`, formData);
      alert(`Response: ${response.data.message || 'Update successful!'}`);
      setIsEditing(false); // Return to the initial state
      setFormData({ streaming_URL: '', email: '' }); // Clear form data
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.message || 'Failed to update configuration'}`);
    }
  };

  return (
    <div>
      {isEditing ? (
        <div>
          <div>
            <label>Streaming URL:</label>
            <input
              type="text"
              name="streaming_URL"
              value={formData.streaming_URL}
              onChange={handleInputChange}
              placeholder="Enter streaming URL"
            />
          </div>
          <div>
            <label>Email:</label>
            <input
              type="text"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="Enter email"
            />
          </div>
          <button onClick={handleSave}>Save</button>
        </div>
      ) : (
        <button onClick={() => setIsEditing(true)}>Edit URL and email</button>
      )}
    </div>
  );
}

  