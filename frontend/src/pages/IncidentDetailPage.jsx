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
        setIncident(res.data.case);
        const grouped = res.data.related_precedents || {};
        setPrecedents(grouped);
      })
      .catch(err => console.error('사건 상세 정보 불러오기 실패:', err));
  }, [id]);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (!incident) return <p style={{ textAlign: 'center' }}>📄 사건 정보를 불러오는 중...</p>;

  return (
    <div style={{ maxWidth: '900px', margin: '40px auto', padding: '30px', background: '#fff', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}>
      <h1 style={{ marginBottom: '12px', fontSize: '24px', color: '#222' }}>{incident.title}</h1>
      <p style={{ color: '#777', fontSize: '14px', marginBottom: '24px' }}>🗓️ {incident.date}</p>

      <section style={{ marginBottom: '30px' }}>
        <h3 style={{ fontSize: '18px', marginBottom: '6px' }}>📝 요약</h3>
        <p style={{ lineHeight: '1.7', color: '#333' }}>{incident.summary}</p>
      </section>

      {incident.content && (
        <section style={{ marginBottom: '30px' }}>
          <h3 style={{ fontSize: '18px', marginBottom: '6px' }}>📄 본문 전체</h3>
          <p style={{ lineHeight: '1.7', color: '#333', whiteSpace: 'pre-line' }}>{incident.content}</p>
        </section>
      )}

      {incident.uri && (
        <a
          href={incident.uri}
          target="_blank"
          rel="noreferrer"
          style={{ display: 'inline-block', margin: '10px 0 30px', fontWeight: 'bold', color: '#007BFF' }}
        >
          🔗 전체 기사 보기
        </a>
      )}

      <section style={{ marginBottom: '30px' }}>
        <h3 style={{ fontSize: '18px', marginBottom: '6px' }}>📘 관련 법률</h3>
        {incident.related_laws?.length ? (
          <ul style={{ paddingLeft: '20px', color: '#444' }}>
            {incident.related_laws.map((law, idx) => (
              <li key={idx}>{law}</li>
            ))}
          </ul>
        ) : <p style={{ color: '#777' }}>관련 법률 없음</p>}
      </section>

      <section>
        <h3 style={{ fontSize: '18px', marginBottom: '12px' }}>⚖️ 관련 판례</h3>
        {Object.keys(precedents).length ? (
          Object.entries(precedents).map(([law, items], idx) => (
            <div key={idx} style={{ marginBottom: '24px', padding: '12px 16px', background: '#fafafa', borderRadius: '8px', border: '1px solid #eee' }}>
              <h4 style={{ marginBottom: '10px', color: '#555' }}>📌 {law}</h4>
              <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
                {items.map((p, i) => (
                  <li key={i} style={{ padding: '8px 0', borderBottom: '1px dashed #ddd' }}>
                    <a href={p.url} target="_blank" rel="noreferrer" style={{ fontWeight: 'bold', color: '#333' }}>
                      {p.title}
                    </a>
                    <div style={{ fontSize: '13px', color: '#777' }}>{p.court} | {p.date}</div>
                  </li>
                ))}
              </ul>
            </div>
          ))
        ) : <p style={{ color: '#777' }}>관련 판례 없음</p>}
      </section>

      {/* ✅ TOP 버튼 */}
      <button
        onClick={scrollToTop}
        style={{
          position: 'fixed',
          bottom: '40px',
          right: '40px',
          padding: '12px 20px',
          fontSize: '14px',
          backgroundColor: '#007BFF',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
          cursor: 'pointer',
          zIndex: 1000
        }}
      >
        ⬆ TOP
      </button>
    </div>
  );
}

export default IncidentDetailPage;
