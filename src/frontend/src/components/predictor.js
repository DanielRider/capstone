import React, { useState } from 'react';
import axios from 'axios';
/* react compenent that displays results when we get them from the backend*/
function Predictor() {
    const [inputData, setInputData] = useState({});
    const [result, setResult] = useState(null);

    const handlePredict = async () => {
        try {
            const response = await axios.post('/api/predict', inputData);
            setResult(response.data);
        } catch (error) {
            console.error("An error occurred while fetching data", error);
        }
    }

    return (
        <div>
            {/* Your input fields here */}
            <button onClick={handlePredict}>Predict</button>
            {result && (
                <div>
                    <h2>Result:</h2>
                    <p>{JSON.stringify(result)}</p>
                </div>
            )}
        </div>
    );
}

export default Predictor;
