from flask import Flask,request,jsonify
import pickle
import pandas as pd
app = Flask(__name__)

model = pickle.load(open("model.pkl",'rb'))

@app.route('/')
def index():
    return "Mini project MedAyu symptoms api"

@app.route('/disease', methods=['POST'])
def classify():
    syptoms = request.form.get('syptoms')
    print(syptoms)
    df_norm = pd.read_csv("dis_sym_dataset_norm.csv")
    Y = df_norm.iloc[:, 0:1]
    #added for testing: head
    X = df_norm.iloc[:, 1:]
    dataset_symptoms = list(X.columns)
    sample_x = [0 for x in range(0,len(dataset_symptoms))]
    for val in syptoms:
        sample_x[dataset_symptoms.index(val)]=1
    #added for testing: end
    predicted_disease = model.predict_proba([sample_x])
    k=3
    diseases = list(set(Y['label_dis']))
    diseases.sort()
    topk = predicted_disease[0].argsort()[-k:][::-1]
    result = {'disease':topk[0]}
    return jsonify(result)


if __name__ == '__main__':
    print("Working")
    app.run(debug=True,host="0.0.0.0")