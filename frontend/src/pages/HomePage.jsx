import React, { useEffect, useState } from 'react';
import axios from 'axios';
import NewsCard from '../components/NewsCard';

function HomePage() {
  const [newsList, setNewsList] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/news/summary')
      .then(res => setNewsList(res.data))
      .catch(err => console.error('뉴스 요약 API 오류:', err));
  }, []);

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '20px' }}>📰 요약 뉴스</h1>
      {newsList.length === 0 ? (
        <p>뉴스를 불러오는 중입니다...</p>
      ) : (
        newsList.map((news) => (
          <NewsCard key={news.id} news={news} />
        ))
      )}
    </div>
  );
}

export default HomePage;
