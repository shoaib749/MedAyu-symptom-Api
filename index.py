from flask import Flask,request,jsonify
import pickle
app = Flask(__name__)

model = pickle.load_modle("model.pkl")

@app.route('/')
def index():
    return "Mini project MedAyu symptoms api"

@app.route('/disease', methods=['POST'])
def classify():
    syptoms = request.form.get('syptoms')
    return jsonify(syptoms)


if __name__ == '__main__':
    print("Working")
    app.run(debug=True,host="0.0.0.0")