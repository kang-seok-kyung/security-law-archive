// src/components/SearchBar.jsx
import React, { useState } from 'react';

function SearchBar({ onSearch }) {
  const [keyword, setKeyword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault(); // 새로고침 방지
    onSearch(keyword);  // 부모 컴포넌트로 검색어 전달
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
      <input
        type="text"
        placeholder="검색어를 입력하세요 (예: 해킹)"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        style={{ padding: '8px', width: '300px' }}
      />
      <button type="submit" style={{ marginLeft: '8px', padding: '8px' }}>
        검색
      </button>
    </form>
  );
}

export default SearchBar;
