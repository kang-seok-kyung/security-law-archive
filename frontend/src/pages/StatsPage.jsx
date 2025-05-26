// src/pages/StatsPage.jsx
import React from 'react';
import ChartBox from '../components/ChartBox';

function StatsPage() {
  // 🎯 mock 데이터
  const yearStats = {
    labels: ['2021', '2022', '2023'],
    data: [2, 5, 3]
  };

  const courtStats = {
    labels: ['서울고등법원', '대법원', '서울중앙지방법원'],
    data: [4, 2, 5]
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '40px' }}>
      <h2 style={{ textAlign: 'center' }}>판례 통계 시각화</h2>
      <ChartBox title="연도별 사건 수" labels={yearStats.labels} data={yearStats.data} />
      <ChartBox title="법원별 사건 분포" labels={courtStats.labels} data={courtStats.data} />
    </div>
  );
}

export default StatsPage;
