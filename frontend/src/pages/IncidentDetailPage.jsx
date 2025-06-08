import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function IncidentDetailPage() {
  const { id } = useParams();
  const [incident, setIncident] = useState(null);
  const [precedents, setPrecedents] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/api/cases/${id}`)
      .then(res => {
        setIncident(res.data.case);
        setPrecedents(res.data.related_precedents);
      })
      .catch(err => console.error('사건 상세 정보 불러오기 실패:', err));
  }, [id]);

  if (!incident) return <p style={{ textAlign: 'center' }}>📄 사건 정보를 불러오는 중...</p>;

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '40px' }}>
      <h2>{incident.title}</h2>
      <p><strong>날짜:</strong> {incident.date}</p>
      <p><strong>요약:</strong> {incident.summary || '요약 정보 없음'}</p>
      <p>  <strong>관련 법률:</strong>{' '}{Array.isArray(incident.related_law)? incident.related_law.join(', '): incident.related_law || '없음'}</p>


      <h3 style={{ marginTop: '40px' }}>📚 관련 판례</h3>
      <ul style={{ paddingLeft: 0, listStyle: 'none' }}>
        {precedents.map((p, idx) => (
          <li key={idx} style={{
            borderBottom: '1px solid #eee', padding: '10px 0'
          }}>
            <a href={p.url} target="_blank" rel="noreferrer" style={{ fontWeight: 'bold' }}>{p.title}</a>
            <div style={{ fontSize: '14px', color: '#555' }}>
              {p.court} | {p.date}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default IncidentDetailPage;
