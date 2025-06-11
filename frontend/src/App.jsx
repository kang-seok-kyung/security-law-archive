import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import IncidentDetailPage from './pages/IncidentDetailPage';
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
        <Link to="/" style={{ marginRight: '20px', fontWeight: 'bold' }}>📰 사건 목록</Link>
        <Link to="/stats" style={{ fontWeight: 'bold' }}>📊 통계</Link>
      </div>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/incident/:id" element={<IncidentDetailPage />} />
        <Route path="/stats" element={<StatsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
