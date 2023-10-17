from flask import Flask, request, jsonify
import my_model  # pickle... whatever here
#basically this is where we take a json from the frontend then
#we run it through the model. Then return the results to frontend
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    result = my_model.predict(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)

