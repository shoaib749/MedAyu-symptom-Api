<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️-->
[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)](#medayu-symptom-api)

# ➤ MedAyu Symptom API

MedAyu Symptom API is a Flask application that utilizes Keras and machine learning models to predict diseases based on patient symptoms. This backend application provides API endpoints for the Android application called "MedAyu". The Android application takes symptoms as input and predicts diseases, recommending Ayurvedic plants based on the disease.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#api-endpoints)

## ➤ API Endpoints

1. Ayurvedic plant detection using leaf images:
   - API: [https://flask-production-0d46.up.railway.app/class](https://flask-production-0d46.up.railway.app/class)
   - Method: POST
   - Parameter: test_url (URL)
   - Response: result (JSON Object)

2. Symptoms synonyms generator:
   - API: [https://web-production-aeed.up.railway.app/EnterSymptoms](https://web-production-aeed.up.railway.app/EnterSymptoms)
   - Method: POST
   - Parameter: user_symptoms (Array)
   - Response: result (JSON Object)

3. Co-occurring symptoms generator:
   - API: [https://web-production-aeed.up.railway.app/db](https://web-production-aeed.up.railway.app/db)
   - Method: POST
   - Parameter: request (Array)
   - Response: result (JSON Object)

4. Disease detection based on symptoms:
   - API: [https://web-production-aeed.up.railway.app/disease](https://web-production-aeed.up.railway.app/disease)
   - Method: POST
   - Parameter: symptoms (Array)
   - Response: result (JSON Object)


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#website-link)

## ➤ Website Link

Visit the website at [https://web-production-aeed.up.railway.app/](https://web-production-aeed.up.railway.app/).

Please note that the provided information is subject to change or update.
