from fastapi import FastAPI,Path,HTTPException,Query
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal

app=FastAPI()
class patient(BaseModel):
    id=Annotated[str,Field(...,description='ID of the patient',examples='P001')]
    name=Annotated[str,Field(...,description='name of the patient')]
    city=Annotated[str,Field(...,description='city where patient is living')]
    age=Annotated[int,Field(gt=0,lt=120,description='age of the patient')]
    gender=Annotated[Literal['male','female','others'],Field(...,description='gender of the patient')]
    height=Annotated[float,Field(...,gt=0,description='height of the patient in mtrs')]
    weight=Annotated[float,Field(...,gt=0,description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round((self.weight/(self.height**2)),2)
        return bmi
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return 'normal'
        elif self.bmi<30:
            return 'normal'
        else:
            return 'obese'

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
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data



