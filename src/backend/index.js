/* this is where we take in the results fron the front end and 
 * send it to the model*/
const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;

app.use(express.json());
app.post('/api/predict', async (req, res) => {
    try {
        const pythonApiUrl = 'http://localhost:5000/predict';
        const response = await axios.post(pythonApiUrl, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).send(error.toString());
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
