import React, { useEffect, useState } from 'react';
import axios from 'axios';

function StatsPage() {
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/api/stats`)
      .then(res => {
        setStats(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('통계 불러오기 실패:', err);
        setError('통계 정보를 불러오는 데 실패했습니다.');
        setLoading(false);
      });
  }, []);

  if (loading) return <p style={{ textAlign: 'center' }}>📊 통계 데이터를 불러오는 중...</p>;
  if (error) return <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '40px', textAlign: 'center' }}>
      <h2>📊 위반 법률별 판례 통계</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '30px' }}>
        <thead>
          <tr>
            <th style={{ borderBottom: '1px solid #ccc', padding: '10px' }}>법률명</th>
            <th style={{ borderBottom: '1px solid #ccc', padding: '10px' }}>관련 판례 수</th>
          </tr>
        </thead>
        <tbody>
          {stats.map((item, idx) => (
            <tr key={idx}>
              <td style={{ padding: '10px', textAlign: 'left' }}>{item.law}</td>
              <td style={{ padding: '10px' }}>{item.count}건</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default StatsPage;
