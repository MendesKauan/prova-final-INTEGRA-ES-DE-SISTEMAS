const express = require('express');
const redis = require('redis');
const axios = require('axios'); 

const app = express();
const port = 3000;

app.use(express.json());

const cacheRedis = redis.createClient({ url: 'redis://localhost:6379' });
(async () => { await cacheRedis.connect(); })();


app.get('/sensor-data', async (req, res) => {
  const cacheKey = 'sensor-data'; 
  const cachedData = await cacheRedis.get(cacheKey); 

  if (cachedData) { return res.json(JSON.parse(cachedData)); }

  const simulatedData = {
    temperature: (Math.random() * 50 + 10).toFixed(2), 
    pressure: (Math.random() * 1000 + 500).toFixed(2),  
    timestamp: new Date().toISOString()                 
  };

  await cacheRedis.setEx(cacheKey, 10, JSON.stringify(simulatedData));
  res.json(simulatedData); 
});

app.post('/alert', async (req, res) => {
  const { alert } = req.body; 

  const alertData = {
    message: alert,
    timestamp: new Date().toISOString()
  };

  await axios.post('http://localhost:5000/event', alertData);
  res.status(200).json({ message: 'Alerta enviado para API Python.' }); 
});

app.listen(port, () => {
  console.log(`API Node.js de Sensores rodando em http://localhost:${port}`);
});