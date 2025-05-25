import React from 'react'; // 16 이하 구버전 react일 경우 필요
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';


function App() {
  return (
    <Router>
      <div style={{
        padding: '20px',
        textAlign: 'center',
        borderBottom: '1px solid #ddd',
        marginBottom: '20px'
      }}>
        <Link to="/" style={{ marginRight: '20px', textDecoration: 'none', fontWeight: 'bold' }}>🔍 판례 검색</Link>
        <Link to="/stats" style={{ textDecoration: 'none', fontWeight: 'bold' }}>📊 통계 보기</Link>
      </div>

    </Router>
  );
}

export default App;