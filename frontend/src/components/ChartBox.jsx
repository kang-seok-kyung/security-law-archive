// src/components/ChartBox.jsx
import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function ChartBox({ title, labels, data }) {
  return (
    <div style={{ marginBottom: '40px' }}>
      <h3>{title}</h3>
      <Bar
        data={{
          labels: labels,
          datasets: [
            {
              label: title,
              data: data,
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderRadius: 5
            }
          ]
        }}
        options={{
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            title: { display: false },
          },
        }}
      />
    </div>
  );
}

export default ChartBox;
