from fastapi import FastAPI,Path
import json

app=FastAPI()

def load_data():
    with open ('patient.json','r') as f:
        data=json.load(f)

    return data

@app.get("/")
def hello():
    return{'message':'patient management system api'}

@app.get('/about')
def about():
    return {'message':'a fully functional API to manage patient record '}

@app.get('/view')
def view():
    data=load_data()

    return data
@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='ID of the patient in db',example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    return {'error':'patient is not found'}

