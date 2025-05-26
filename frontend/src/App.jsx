// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import StatsPage from './pages/StatsPage';

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

      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/stats" element={<StatsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
