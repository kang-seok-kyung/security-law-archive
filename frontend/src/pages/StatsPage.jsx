import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ChartBox from '../components/ChartBox';

function StatsPage() {
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/api/stats/cases/by-law`)
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

  // 데이터 변환
  const labels = Object.keys(stats);
  const data = Object.values(stats);

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '40px', textAlign: 'center' }}>
      <h2>📊 위반 법률별 사건 통계</h2>

      {/* ✅ 차트 */}
      <ChartBox title="📊 위반 법률별 사건 수" labels={labels} data={data} />

      {/* ✅ 표 */}
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '30px' }}>
        <thead>
          <tr>
            <th style={{ borderBottom: '1px solid #ccc', padding: '10px' }}>법률명</th>
            <th style={{ borderBottom: '1px solid #ccc', padding: '10px' }}>관련 사건 수</th>
          </tr>
        </thead>
        <tbody>
          {labels.map((law, idx) => (
            <tr key={idx}>
              <td style={{ padding: '10px', textAlign: 'left' }}>{law}</td>
              <td style={{ padding: '10px' }}>{data[idx]}건</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default StatsPage;
