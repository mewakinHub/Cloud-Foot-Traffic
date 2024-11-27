'use client';

import React, { useState } from "react";
import api from "../../../utils/api"; // Adjust the path based on your project structure

const ResultManagement: React.FC = () => {
  // State for /create/result form
  const [createData, setCreateData] = useState({
    username: "",
    config: "",
    result: "",
    image_url: "",
  });

  // State for /delete/result/{username}
  const [deleteUsername, setDeleteUsername] = useState("");

  // Handle /create/result submit
  const handleCreateSubmit = async () => {
    try {
      const response = await api.post("/create/result", createData);
      alert(`Result created successfully: ${JSON.stringify(response.data)}`);
    } catch (error: any) {
      console.error(error);
      alert(`Error creating result: ${error.response?.data?.detail || error.message}`);
    }
  };

  // Handle /delete/result/{username} submit
  const handleDeleteSubmit = async () => {
    try {
      const response = await api.delete(`/delete/result/${deleteUsername}`);
      alert(`All results from user ${deleteUsername} deleted successfully!`);
      setDeleteUsername(""); // Reset username field
    } catch (error: any) {
      console.error(error);
      alert(`Error deleting results: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div>
      {/* Create Result Form */}
      <div>
        <h2>Create Result</h2>
        <div>
          <label>
            Username:
            <input
              type="text"
              value={createData.username}
              onChange={(e) => setCreateData({ ...createData, username: e.target.value })}
              placeholder="Enter username"
            />
          </label>
        </div>
        <div>
          <label>
            Config:
            <input
              type="text"
              value={createData.config}
              onChange={(e) => setCreateData({ ...createData, config: e.target.value })}
              placeholder="Enter config"
            />
          </label>
        </div>
        <div>
          <label>
            Result:
            <input
              type="number"
              value={createData.result}
              onChange={(e) => setCreateData({ ...createData, result: e.target.value })}
              placeholder="Enter result (can be blank)"
            />
          </label>
        </div>
        <div>
          <label>
            Image URL:
            <input
              type="text"
              value={createData.image_url}
              onChange={(e) => setCreateData({ ...createData, image_url: e.target.value })}
              placeholder="Enter image URL"
            />
          </label>
        </div>
        <button onClick={handleCreateSubmit}>Submit</button>
      </div>

      {/* Delete Result Form */}
      <div>
        <h2>Delete All Results from User</h2>
        <div>
          <label>
            Username:
            <input
              type="text"
              value={deleteUsername}
              onChange={(e) => setDeleteUsername(e.target.value)}
              placeholder="Enter username"
            />
          </label>
        </div>
        <button onClick={handleDeleteSubmit}>Delete all result from this user</button>
      </div>
    </div>
  );
};

export default ResultManagement;
