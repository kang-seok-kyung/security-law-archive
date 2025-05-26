import React from 'react';

function CaseCard({ data }) {
  console.log('받은 판례 데이터:', data);

  const id = data.id || data.판례일련번호;

  // OC 키 포함된 실제 API 전문 보기 링크
  const detailUrl = id
    ? `https://www.law.go.kr/DRF/lawService.do?target=prec&ID=${id}&type=HTML&OC=sk6461@naver.com`
    : '#';

  return (
    <div style={{
      border: '1px solid #ccc',
      borderRadius: '8px',
      padding: '16px',
      marginBottom: '16px',
      backgroundColor: '#f9f9f9',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <h3 style={{ marginBottom: '8px' }}>
        {data.title || data.사건명 || '제목 없음'}
      </h3>

      <p><strong>법원명:</strong> {data.court || data.법원명 || '알 수 없음'}</p>
      <p><strong>선고일자:</strong> {data.date || data.선고일자 || '알 수 없음'}</p>

      <a
        href={detailUrl}
        target="_blank"
        rel="noopener noreferrer"
        style={{
          display: 'inline-block',
          marginTop: '10px',
          color: '#007BFF',
          textDecoration: 'none',
          fontWeight: 'bold'
        }}
      >
        📄 판례 전문 보기
      </a>
    </div>
  );
}

export default CaseCard;
