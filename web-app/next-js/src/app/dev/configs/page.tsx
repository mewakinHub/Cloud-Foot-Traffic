'use client';
import { useEffect, useState, ReactNode } from 'react';
import api from '../../../utils/api';

const ConfigTablePage = () => {
  const [configData, setConfigData] = useState<any[]>([]);
  const [editingRowIndex, setEditingRowIndex] = useState<number | null>(null);
  const [editedData, setEditedData] = useState<{ streaming_URL?: string; email?: string }>({});
  const [showDeleteDialog, setShowDeleteDialog] = useState<{ visible: boolean; index: number | null; username: string | null }>({ visible: false, index: null, username: null });
  const [newUserData, setNewUserData] = useState<{ username: string; Monitoring_status: number; streaming_URL: string; email: string }>({ username: '', Monitoring_status: 0, streaming_URL: '', email: '' });

  useEffect(() => {
    const fetchConfigData = async () => {
      try {
        const response = await api.get('/read/configs');
        setConfigData(response.data);
      } catch (error: any) {
        console.error('Error fetching config data:', error);
      }
    };

    fetchConfigData();
  }, []);

  const handleEditClick = (index: number, item: any) => {
    setEditingRowIndex(index);
    setEditedData({ streaming_URL: item.streaming_URL, email: item.email });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setEditedData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSaveClick = async (index: number) => {
    const updatedData = [...configData];
    updatedData[index] = { ...updatedData[index], ...editedData };
    setConfigData(updatedData);
    setEditingRowIndex(null);

    try {
      await api.put(`/update/config/${updatedData[index].username}`, editedData);
    } catch (error: any) {
      console.error('Error updating config data:', error);
    }
  };

  const handleDeleteClick = (index: number, username: string) => {
    setShowDeleteDialog({ visible: true, index, username });
  };

  const handleConfirmDelete = async () => {
    if (showDeleteDialog.index !== null && showDeleteDialog.username !== null && showDeleteDialog.username.trim() !== '') {
      try {
        await api.delete(`/delete/config/${showDeleteDialog.username}`);
        const updatedData = configData.filter((_, idx) => idx !== showDeleteDialog.index);
        setConfigData(updatedData);
      } catch (error: any) {
        console.error('Error deleting config data:', error);
        alert(`Error deleting config data: ${error.message}`);
      }
    } else {
      alert('Invalid username. Unable to delete.');
    }
    setShowDeleteDialog({ visible: false, index: null, username: null });
  };

  const handleCancelDelete = () => {
    setShowDeleteDialog({ visible: false, index: null, username: null });
  };

  const handleNewUserChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setNewUserData((prev) => ({ ...prev, [name]: value }));
  };

  const handleCreateUser = async () => {
    try {
      await api.post('/create/config/', { ...newUserData, Monitoring_status: 0 });
      setConfigData((prev) => [...prev, { ...newUserData, Monitoring_status: 0 }]);
      setNewUserData({ username: '', Monitoring_status: 0, streaming_URL: '', email: '' });
    } catch (error: any) {
      console.error('Error creating new user:', error);
      alert(`Error creating new user: ${error.message}`);
    }
  };

  return (
    <div>
      <h1>Configuration Data</h1>
      {configData.length > 0 ? (
        <table>
          <thead>
            <tr>
              {Object.keys(configData[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {configData.map((item, index) => (
              <tr key={index}>
                {Object.keys(item).map((key, idx) => (
                  <td key={idx}>
                    {editingRowIndex === index && (key === 'streaming_URL' || key === 'email') ? (
                      <input
                        type="text"
                        name={key}
                        value={editedData[key] || ''}
                        onChange={handleInputChange}
                      />
                    ) : (
                      String(item[key]) as ReactNode
                    )}
                  </td>
                ))}
                <td>
                  {editingRowIndex === index ? (
                    <button onClick={() => handleSaveClick(index)}>Save</button>
                  ) : (
                    <>
                      <button onClick={() => handleEditClick(index, item)}>Edit</button>
                      <button onClick={() => handleDeleteClick(index, item.username)}>Delete</button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Loading...</p>
      )}

      {showDeleteDialog.visible && (
        <div className="delete-dialog">
          <p>Are you sure you want to delete the username {showDeleteDialog.username}?</p>
          <button onClick={handleConfirmDelete}>Yes</button>
          <button onClick={handleCancelDelete}>No</button>
        </div>
      )}

      <div className="create-user-form">
        <h2>Create New User</h2>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={newUserData.username}
          onChange={handleNewUserChange}
        />
        <input
          type="text"
          name="streaming_URL"
          placeholder="Streaming URL"
          value={newUserData.streaming_URL}
          onChange={handleNewUserChange}
        />
        <input
          type="text"
          name="email"
          placeholder="Email"
          value={newUserData.email}
          onChange={handleNewUserChange}
        />
        <button onClick={handleCreateUser}>Create User</button>
      </div>
    </div>
  );
};

export default ConfigTablePage;
