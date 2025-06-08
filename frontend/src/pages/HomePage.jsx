import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function HomePage() {
  const [cases, setCases] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
  axios.get(`${process.env.REACT_APP_API_URL}/api/cases`)
    .then(res => {
      console.log('응답 확인:', res.data);
      setCases(res.data);
    })
    .catch(err => {
      console.error('사건 목록 불러오기 실패:', err);
    });
}, []);


  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '40px' }}>
      <h2>📰 보안 사건 사고 목록</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {cases.map((item) => (
          <li
            key={item._id}
            onClick={() => navigate(`/incident/${item._id}`)}
            style={{
              border: '1px solid #ddd',
              borderRadius: '10px',
              padding: '20px',
              marginBottom: '20px',
              cursor: 'pointer',
              backgroundColor: '#f9f9f9'
            }}
          >
            <h3>{item.title}</h3>
            <p style={{ color: '#777' }}>{item.date}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default HomePage;
