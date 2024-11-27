'use client';

import React, { useEffect, useRef, useState } from "react";
import Chart, { ChartConfiguration } from 'chart.js/auto';
import api from "../../utils/api";

interface GraphProps {
  username: string; // Username passed as a prop
}

const Graph: React.FC<GraphProps> = ({ username }) => {
  const chartRef = useRef<HTMLCanvasElement | null>(null);
  const [chartInstance, setChartInstance] = useState<Chart | null>(null);

  useEffect(() => {
    if (username) {
      fetchResults();
    }
  }, [username]);

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

  return (
    <div>
      <div>
        <canvas
         
        ref={chartRef} />
      </div>
    </div>
  );
};

export default Graph;
