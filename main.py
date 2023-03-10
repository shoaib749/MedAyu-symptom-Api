from flask import Flask,request,jsonify
import pickle
import pandas as pd
import json
app = Flask(__name__)

model = pickle.load(open("model.pkl",'rb'))

@app.route('/')
def index():
    return "Mini project MedAyu symptoms api"

@app.route('/disease', methods=['POST'])
def classify():
    syptoms = request.form.getlist('syptoms')
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
    print(topk)
    #code for disease name: head
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx,t in  enumerate(topk):
        match_sym=set()
        row = df_norm.loc[df_norm['label_dis'] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx,val in enumerate(row[0]):
            if val!=0:
                match_sym.add(dataset_symptoms[idx])
        prob = (len(match_sym.intersection(set(syptoms)))+1)/(len(set(syptoms))+1)
        # prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    result_disease ={}
    for key in topk_sorted:
        prob = topk_sorted[key]*100
        print(str(j) + " Disease name:",diseases[key], "\tProbability:",str(round(prob, 2))+"%")
        result_disease = dict(No=1,disease=diseases[key])
        topk_index_mapping[j] = key
        j += 1
    result = json.dumps({'result':result_disease})
    
    
    
    #code end
    




    return result


if __name__ == '__main__':
    print("Working")
    app.run(debug=True,host="0.0.0.0")