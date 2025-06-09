import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ChartBox from '../components/ChartBox';

function StatsPage() {
  const [yearStats, setYearStats] = useState({});
  const [lawPrecedentStats, setLawPrecedentStats] = useState({});
  const [lawCaseStats, setLawCaseStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

    console.log('🌐 BASE API URL:', baseURL);

    Promise.all([
      axios.get(`${baseURL}/api/stats/precedents/by-year`),
      axios.get(`${baseURL}/api/stats/precedents/by-law`),
      axios.get(`${baseURL}/api/stats/cases/by-law`)
    ])
      .then(([yearRes, lawPrecRes, lawCaseRes]) => {
        console.log('📊 연도별 응답:', yearRes.data);
        console.log('📊 법별 판례 응답:', lawPrecRes.data);
        console.log('📊 법별 사건 응답:', lawCaseRes.data);

        setYearStats(yearRes.data);
        setLawPrecedentStats(lawPrecRes.data);
        setLawCaseStats(lawCaseRes.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('❌ 통계 로딩 실패:', err);
        setError('통계 정보를 불러오는 데 실패했습니다.');
        setLoading(false);
      });
  }, []);

  // dict → labels & data 변환 함수
  const formatStatDict = (stat) => ({
    labels: Object.keys(stat),
    data: Object.values(stat),
  });

  if (loading) return <p style={{ textAlign: 'center' }}>📊 통계 데이터를 불러오는 중...</p>;
  if (error) return <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '40px', textAlign: 'center' }}>
      {/* 📈 연도별 판례 */}
      <h2>📈 연도별 판례 통계</h2>
      <ChartBox title="연도별 판례 수" {...formatStatDict(yearStats)} />
      <DataTable title="연도" stat={yearStats} />

      {/* 📊 법별 판례 */}
      <h2 style={{ marginTop: '60px' }}>📊 법별 판례 통계</h2>
      <ChartBox title="법별 판례 수" {...formatStatDict(lawPrecedentStats)} />
      <DataTable title="법률명" stat={lawPrecedentStats} />

      {/* 🧾 법별 사건 */}
      <h2 style={{ marginTop: '60px' }}>🧾 법별 사건 통계</h2>
      <ChartBox title="법별 사건 수" {...formatStatDict(lawCaseStats)} />
      <DataTable title="법률명" stat={lawCaseStats} />
    </div>
  );
}

// ✅ 테이블도 dict 대응 버전으로 수정
function DataTable({ title, stat }) {
  const keys = Object.keys(stat);
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '30px' }}>
      <thead>
        <tr>
          <th style={{ borderBottom: '1px solid #ccc', padding: '10px' }}>{title}</th>
          <th style={{ borderBottom: '1px solid #ccc', padding: '10px' }}>관련 수</th>
        </tr>
      </thead>
      <tbody>
        {keys.map((key, idx) => (
          <tr key={idx}>
            <td style={{ padding: '10px', textAlign: 'left' }}>{key}</td>
            <td style={{ padding: '10px' }}>{stat[key]}건</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default StatsPage;
