from bs4 import BeautifulSoup
from flask import Flask,request,jsonify,render_template
import pickle
import pandas as pd
import json
from itertools import combinations
import requests
from nltk.corpus import wordnet 
import nltk
import operator
from collections import Counter
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer



    
app = Flask(__name__)
import nltk
nltk.download('stopwords')
# utlities for pre-processing
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
splitter = RegexpTokenizer(r'\w+')
app = Flask(__name__,template_folder='template')
import nltk
nltk.download('stopwords')
nltk.download('WordNetLemmatizer')
nltk.download('RegexpTokenizer')
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
splitter = RegexpTokenizer(r'\w+')

model = pickle.load(open("model.pkl",'rb'))
##use of common files and variables for predection & symptoms
df_norm = pd.read_csv("dis_sym_dataset_norm.csv")
Y = df_norm.iloc[:, 0:1]
X = df_norm.iloc[:, 1:]
dataset_symptoms = list(X.columns)
#End of common section
def synonyms(term):
    synonyms = []
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.content,  "html.parser")
    try:
        container=soup.find('section', {'class': 'MainContentContainer'}) 
        row=container.find('div',{'class':'css-191l5o0-ClassicContentCard'})
        row = row.find_all('li')
        for x in row:
            synonyms.append(x.get_text())
    except:
        None
    for syn in wordnet.synsets(term):
        synonyms+=syn.lemma_names()
    return set(synonyms)


@app.route('/')
def index():
    # return "Mini project MedAyu symptoms api: 1. /EnterSymptoms using POST Method & params:user_symtoms(Array) 2. /db using POST method with params:request 3. /disease Using POST method & params:syptoms "
    return render_template('index.html')

@app.route('/index.html')
def index_f():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/api.html')
def api():
    return render_template('api.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/check.html/')
def check():
    return render_template('check.html')

@app.route('/check.html/coSymptoms.html/')
def co():
    return render_template('coSymptoms.html')


@app.route('/check.html/coSymptoms.html/result.html/')
def result():
    return render_template('result.html')

@app.route('/disease', methods=['POST'])
def classify():
    syptoms = request.form.getlist('syptoms')
    print(syptoms)
    
    #added for testing: head
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

@app.route('/EnterSymptoms',methods=['POST'])
# def Enter():
#     Symptoms = request.form.getlist('user_symtoms')
#     print(Symptoms)
#     ##taking input is the thing after converting 
#     user_symptoms = []
#     for user_sym in Symptoms:
#         user_sym = user_sym.split()
#         str_sym = set()
#         for comb in range(1, len(user_sym)+1):
#             for subset in combinations(user_sym, comb):
#                 subset=' '.join(subset)
#                 subset = synonyms(subset) 
#                 str_sym.update(subset)
#         str_sym.add(' '.join(user_sym))
#         user_symptoms.append(' '.join(str_sym).replace('_',' '))
#     # Loop over all the symptoms in dataset and check its similarity score to the synonym string of the user-input 
#     # symptoms. If similarity>0.5, add the symptom to the final list
#     found_symptoms = set()
#     for idx, data_sym in enumerate(dataset_symptoms):
#         data_sym_split=data_sym.split()
#         for user_sym in user_symptoms:
#             count=0
#             for symp in data_sym_split:
#                 if symp in user_sym.split():
#                     count+=1
#             if count/len(data_sym_split)>0.5:
#                 found_symptoms.add(data_sym)
#     found_symptoms = list(found_symptoms)
#     result = json.dumps({'result':found_symptoms})
#     return result
# # returns the list of synonyms of the input word from thesaurus.com (https://www.thesaurus.com/) and wordnet (https://www.nltk.org/howto/wordnet.html)
# #testing new user_symptoms method
def Enter():
    Symptoms = str(request.form.get('user_symtoms')).lower().split(',')
    print(Symptoms)
    ##taking input is the thing after converting 
    processed_user_symptoms=[]
    for sym in Symptoms:
        sym=sym.strip()
        sym=sym.replace('-',' ')
        sym=sym.replace("'",'')
        sym = ' '.join([lemmatizer.lemmatize(word) for word in splitter.tokenize(sym)])
    processed_user_symptoms.append(sym)

    user_symptoms = []
    for user_sym in processed_user_symptoms:
        user_sym = user_sym.split()
        str_sym = set()
        for comb in range(1, len(user_sym)+1):
            for subset in combinations(user_sym, comb):
                subset=' '.join(subset)
                subset = synonyms(subset) 
                str_sym.update(subset)
        str_sym.add(' '.join(user_sym))
        user_symptoms.append(' '.join(str_sym).replace('_',' '))
    # Loop over all the symptoms in dataset and check its similarity score to the synonym string of the user-input 
    # symptoms. If similarity>0.5, add the symptom to the final list
    found_symptoms = set()
    for idx, data_sym in enumerate(dataset_symptoms):
        data_sym_split=data_sym.split()
        for user_sym in user_symptoms:
            count=0
            for symp in data_sym_split:
                if symp in user_sym.split():
                    count+=1
            if count/len(data_sym_split)>0.5:
                found_symptoms.add(data_sym)
    found_symptoms = list(found_symptoms)
    result = json.dumps({'result':found_symptoms})
    return result
# def Enter():
    Symptoms = request.form.getlist('user_symtoms')
    print(Symptoms)
    ##taking input is the thing after converting 
    processed_user_symptoms=[]
    for sym in Symptoms:
        sym=sym.strip()
        sym=sym.replace('-',' ')
        sym=sym.replace("'",'')
        sym = ' '.join([lemmatizer.lemmatize(word) for word in splitter.tokenize(sym)])
    processed_user_symptoms.append(sym)

    user_symptoms = []
    for user_sym in processed_user_symptoms:
        user_sym = user_sym.split()
        str_sym = set()
        for comb in range(1, len(user_sym)+1):
            for subset in combinations(user_sym, comb):
                subset=' '.join(subset)
                subset = synonyms(subset) 
                str_sym.update(subset)
        str_sym.add(' '.join(user_sym))
        user_symptoms.append(' '.join(str_sym).replace('_',' '))
    # Loop over all the symptoms in dataset and check its similarity score to the synonym string of the user-input 
    # symptoms. If similarity>0.5, add the symptom to the final list
    found_symptoms = set()
    for idx, data_sym in enumerate(dataset_symptoms):
        data_sym_split=data_sym.split()
        for user_sym in user_symptoms:
            count=0
            for symp in data_sym_split:
                if symp in user_sym.split():
                    count+=1
            if count/len(data_sym_split)>0.5:
                found_symptoms.add(data_sym)
    found_symptoms = list(found_symptoms)
    result = json.dumps({'result':found_symptoms})
    return result

##code starting for user selection me symptoms from the db
@app.route('/db',methods=['POST'])
def db():
    symptoms = str(request.form.get('request')).lower().split(',')
    print(symptoms)
    dis_list = set() 
    counter_list = []           
    for symp in symptoms:
        dis_list.update(set(df_norm[df_norm[symp]==1]['label_dis']))

    for dis in dis_list:
        row = df_norm.loc[df_norm['label_dis'] == dis].values.tolist()
        row[0].pop(0)
        for idx,val in enumerate(row[0]):
            if val!=0 and dataset_symptoms[idx] not in symptoms:
                counter_list.append(dataset_symptoms[idx])
    # Symptoms that co-occur with the ones selected by user              
    dict_symp = dict(Counter(counter_list))
    dict_symp_tup = sorted(dict_symp.items(), key=operator.itemgetter(1),reverse=True)   
    # print(dict_symp_tup) 
    result = json.dumps({'result':dict_symp_tup})
    return result



if __name__ == '__main__':
    print("Working")
    app.run(debug=True,host="0.0.0.0")

#test