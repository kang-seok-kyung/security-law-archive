import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function IncidentDetailPage() {
  const { id } = useParams();
  const [incident, setIncident] = useState(null);
  const [precedents, setPrecedents] = useState({});

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/api/cases/${id}`)
      .then(res => {
        console.log("📦 사건 상세 응답:", res.data);
        setIncident(res.data.case);

        const grouped = res.data.related_precedents;
        if (grouped && typeof grouped === 'object') {
          setPrecedents(grouped);
        } else {
          setPrecedents({});
        }
      })
      .catch(err => console.error('사건 상세 정보 불러오기 실패:', err));
  }, [id]);

  if (!incident) return <p style={{ textAlign: 'center' }}>📄 사건 정보를 불러오는 중...</p>;

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '40px' }}>
      <h2>{incident.title}</h2>
      <p><strong>날짜:</strong> {incident.date}</p>
      <p><strong>요약:</strong> {incident.summary || '요약 정보 없음'}</p>

      {/* 📄 기사 본문 출력 */}
      {incident.content && (
        <div style={{ marginTop: '20px', whiteSpace: 'pre-line', lineHeight: 1.6 }}>
          <strong>📄 본문 전체:</strong>
          <p>{incident.content}</p>
        </div>
      )}

      {/* 🔗 전체 기사 보기 링크 (uri 사용) */}
      {incident.uri && (
        <a
          href={incident.uri}
          target="_blank"
          rel="noreferrer"
          style={{
            display: 'inline-block',
            margin: '10px 0',
            fontWeight: 'bold',
            color: '#007BFF'
          }}
        >
          🔗 전체 기사 보기
        </a>
      )}

      {/* 📘 관련 법률 */}
      <div style={{ marginTop: '20px' }}>
        <strong>관련 법률:</strong>
        {Array.isArray(incident.related_laws) && incident.related_laws.length > 0 ? (
          <ul style={{ paddingLeft: '20px', marginTop: '5px' }}>
            {incident.related_laws.map((law, idx) => (
              <li key={idx}>{law}</li>
            ))}
          </ul>
        ) : (
          <span style={{ color: '#777', marginLeft: '8px' }}>없음</span>
        )}
      </div>

      {/* ⚖️ 관련 판례 (법률별로 구분) */}
      <h3 style={{ marginTop: '40px' }}>📚 관련 판례</h3>
      {precedents && typeof precedents === 'object' && Object.keys(precedents).length > 0 ? (
        Object.entries(precedents).map(([law, list], idx) => (
          <div key={idx} style={{ marginBottom: '30px' }}>
            <h4 style={{ color: '#444' }}>📌 {law}</h4>
            <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
              {list.map((p, pIdx) => (
                <li key={pIdx} style={{ borderBottom: '1px solid #eee', padding: '10px 0' }}>
                  <a href={p.url} target="_blank" rel="noreferrer" style={{ fontWeight: 'bold' }}>
                    {p.title}
                  </a>
                  <div style={{ fontSize: '14px', color: '#555' }}>
                    {p.court} | {p.date}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ))
      ) : (
        <p style={{ color: '#777' }}>📄 관련 판례 없음</p>
      )}
    </div>
  );
}

export default IncidentDetailPage;
