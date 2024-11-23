'use client';

import React, { useEffect, useRef, useState } from "react";
import Chart, { ChartConfiguration } from 'chart.js/auto';
import api from "../../../utils/api";

const UserResultsGraph: React.FC = () => {
  const chartRef = useRef<HTMLCanvasElement | null>(null);
  const [chartInstance, setChartInstance] = useState<Chart | null>(null);
  const [username, setUsername] = useState("");
  const [usernames, setUsernames] = useState<string[]>([]);

  useEffect(() => {
    fetchUsernames();
  }, []);

  useEffect(() => {
    if (username) {
      fetchResults();
    }
  }, [username]);

  const fetchUsernames = async () => {
    try {
      const response = await api.get("/read/configs");
      const data: { username: string }[] = response.data;
      setUsernames(data.map((entry) => entry.username));
    } catch (error: any) {
      console.error(error);
      alert(`Error fetching usernames: ${error.response?.data?.detail || error.message}`);
    }
  };

  const fetchResults = async () => {
    try {
      const response = await api.get(`/read/results/${username}`);
      const data = response.data;

      // Extracting data for graph
      const labels = data.map((entry: any) => entry.DATE_TIME);
      const results = data.map((entry: any) => entry.result);

      const newChartData: ChartConfiguration<'line'> = {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: "User Results Over Time",
              data: results,
              borderColor: "rgba(75,192,192,1)",
              backgroundColor: "rgba(75,192,192,0.2)",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: `Results for ${username}`,
            },
          },
        },
      };

      if (chartRef.current) {
        if (chartInstance) {
          chartInstance.destroy();
        }
        const newInstance = new Chart(chartRef.current, newChartData);
        setChartInstance(newInstance);
      }
    } catch (error: any) {
      console.error(error);
      alert(`Error fetching results: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await api.get(`/download/${username}`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${username}_data.zip`); // Change file extension as needed
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
    } catch (error: any) {
      console.error(error);
      alert(`Error downloading file: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div>
      <h2>Graph User Results</h2>
      <div>
        <label>Username:</label>
        <select
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        >
          <option value="">Select a username</option>
          {usernames.map((user) => (
            <option key={user} value={user}>
              {user}
            </option>
          ))}
        </select>
      </div>
      <div>
        <canvas ref={chartRef} />
      </div>
      {username && (
        <div>
          <button onClick={handleDownload}>Download Data for {username}</button>
        </div>
      )}
    </div>
  );
};

export default UserResultsGraph;
