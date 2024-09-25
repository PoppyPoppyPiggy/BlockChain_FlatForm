const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;

// HTML 파일을 서빙하기 위한 설정
app.use(express.static('public'));

// Python에서 데이터를 가져오는 API 엔드포인트
app.get('/sync-status', async (req, res) => {
  try {
    // Python 서버에서 데이터를 가져오는 부분을 아래에 추가
    const response = await axios.get('http://localhost:5000/status');
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching sync status:', error);
    res.status(500).json({ message: 'Error fetching sync status' });
  }
});

// 서버 실행
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
