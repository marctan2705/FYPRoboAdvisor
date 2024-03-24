const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const app = express();

app.use(bodyParser.json());

app.post('/get-gpt-response', async (req, res) => {
  const userMessage = req.body.userMessage;

  try {
      const response = await axios.post(
        'https://api.openai.com/v1/engines/text-davinci-003/completions',
      {
        prompt: userMessage,
        max_tokens: 50
      },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer YOUR_OPENAI_API_KEY'
        }
      }
    );

    const gptResponse = response.data.choices[0].text;
    res.json({ gptResponse });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'An error occurred' });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
