import React, { useState } from 'react';
import axios from 'axios';
import SearchBar from '../components/SearchBar';
import CaseCard from '../components/CaseCard';

function SearchPage() {
  const [cases, setCases] = useState([]);

  const handleSearch = async (keyword) => {
    try {
      const response = await axios.get('https://www.law.go.kr/DRF/lawSearch.do', {
        params: {
          target: 'prec',
          OC: 'sk6461',             // ✅ 실제 API 키 적용
          type: 'JSON',
          query: keyword,
          section: 2,
          curt: '서울고등법원'
        }
      });

      console.log('API 응답:', response.data);

      // 응답 구조에 맞게 데이터 추출 (테스트 필요)
      const resultArray = response.data.PrecSearch?.prec || [];
      setCases(resultArray);
    } catch (error) {
      console.error('API 요청 실패:', error);
    }
  };

  return (
    <div style={{
      maxWidth: '800px',
      margin: '0 auto',
      padding: '40px',
      textAlign: 'center'
    }}>
      <h2>판례 검색</h2>
      <SearchBar onSearch={handleSearch} />
      <div style={{ textAlign: 'left' }}>
        {cases.length === 0 && <p>검색 결과가 없습니다.</p>}
        {cases.map((item, idx) => (
          <CaseCard key={idx} data={item} />
        ))}
      </div>
    </div>
  );
}

export default SearchPage;
