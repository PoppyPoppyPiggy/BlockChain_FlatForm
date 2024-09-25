const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const app = express();
const port = 5000;

// 상태를 저장할 변수
let syncStatus = {
  currentBlock: 0,
  totalBlocks: 0,
  progress: 0.0,
  addedBlocks: 0,
  addedData: 0.0,
  speed: 0.0,
  transactions: 0,
  eta: 'N/A'
};

// CORS 허용 및 JSON 바디 파싱 설정
app.use(cors());
app.use(bodyParser.json());

// 정적 파일 제공 (CSS, JS, HTML 등)
app.use(express.static(path.join(__dirname, 'public')));

// 클라이언트에서 상태 조회
app.get('/status', (req, res) => {
  res.json(syncStatus);
});

// Python 스크립트에서 상태 업데이트
app.post('/update', (req, res) => {
  const data = req.body;

  if (data && data.currentBlock && data.totalBlocks) {
    syncStatus = data;
    console.log('Sync status updated:', syncStatus);
    res.status(200).send('Sync status received');
  } else {
    res.status(400).send('Invalid sync data');
  }
});

// 클라이언트에서 /index로 접속하면 index.html 파일 제공
app.get('/index', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 서버 실행
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
