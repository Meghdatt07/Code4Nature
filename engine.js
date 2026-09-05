// engine.js - simple Express server for Code4Nature demo
// Run: node engine.js

const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Code4Nature engine running');
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(port, () => {
  console.log(`Engine listening on port ${port}`);
});
