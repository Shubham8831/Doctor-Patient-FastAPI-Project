from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

#Pydantic model for adding new patient data
class Patient(BaseModel):
    # Define fields with types, validation, and examples
    id : Annotated[str, Field(..., description='ID of the patient', examples=["P001"])]
    name: Annotated[str, Field(..., description='name of the patient', examples=['ramesh'])]
    city: Annotated[str, Field(..., description='city where patient lives', examples=["jaipur"])]
    age: Annotated[int, Field(..., gt=0, lt=120, description='enter age of patient', examples=[50])]
    gender: Annotated[Literal["male", "female", "others"], Field(..., description="enter gender of the patient", examples=["male"])]
    height:Annotated[float, Field(..., gt=0, lt=10, description='enter the height of patient in meters', examples=[3.2])]
    weight:Annotated[float, Field(..., gt=0, lt=500, description="enter the weight of patient in kgs", examples=[55.6])]

    # Compute BMI using weight and height
    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi = round((self.weight / (self.height)**2), 2)
        return bmi
    
     # Compute verdict based on BMI
    @computed_field
    @property
    def verdict(self) -> str:

        if self.calculate_bmi < 18.5:
            return 'Underweight'
        elif self.calculate_bmi < 25:
            return 'Normal'
        elif self.calculate_bmi < 30:
            return 'Normal'
        else:
            return 'Obese'



#pydantic model for updating existing patient data
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[str], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]



# Function to load data from the JSON file
def load_data(): 
    with open("patients.json", 'r') as f:
        data = json.load(f)  # Read JSON file and convert to dictionary
    return data

# Function to save data to the JSON file
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)  # Save dictionary to JSON file





#HOME

# Route to show welcome message
@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

# Route to show about info
@app.get("/about")
def about():
    return {"message":"A fully functional API to manage patient records"}

# Route to view all patients
@app.get("/view")
def view():
    data = load_data()
    return data




#Path Parameter
# Route to view a specific patient by ID (Path Parameter)
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description = "this takes a patient id ", example = "P001")):
    #load all patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code= 404, detail= "patient not found")




#Query Parameter
# Route to sort patients based on height, weight, or bmi (Query Parameters)
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description = "sort on the basics of height, weight or bmi"), order: str = Query('asc', description='sort in ascending or descending order')):

    # Check if sort_by field is valid
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'invalid field select from {valid_fields}')

    # Check if order is valid
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="invalid order select between asc and desc")

    data = load_data()  # Load patient data

    # Set sort order
    sort_order = True if order == "desc" else False

    # Sort the data based on requested field and order
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data  # Return sorted list




#POST

# Route to create/add a new patient (POST)
@app.post("/create")
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #check if patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail='patient already exist')

    # if not add to database
    # first we have to convert the pydantic object to dictionary
    # Convert patient model to dictionary (excluding 'id') and add to data
    data[patient.id] = patient.model_dump(exclude=["id"])    # bmi and verdict already calculated and added in backend

    # Convert model to dictionary to include computed fields (try h yea)
    # patient_dict = patient.model_dump()
    # patient_dict["bmi"] = patient.bmi
    # patient_dict["verdict"] = patient.verdict

    # data[patient.id] = patient_dict


    #save into json file using save data function
    save_data(data)
    
    # now tell client that work has been done
    return JSONResponse(status_code=201, content={"message": 'patient added to database successfully'})



#PUT

#update endpoint
@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update:PatientUpdate):
    
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")
    
    existing_patient_info = data[patient_id]

    #patient update in dict
    updated_patient_info =patient_update.model_dump(exclude_unset=True) # this dict will have only field to be updated also no default value will be sent

    #loop over update patient info and update existing patient info 
    for key, Value in updated_patient_info.items():
        existing_patient_info[key] = Value

    # problem = we needed to update the bmi and verdict
    # existing patient info -> pydantic object (with help of Patient model) -> we get updated bmi and verdict -> we get new pydantic object -> convert it to dict.
    
    # we also need to add id as it will not be present in existing patient info
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info) # new pydantic object
    existing_patient_info = patient_pydantic_object.model_dump(exclude=['id'])

    # add this to data
    data[patient_id] = existing_patient_info


    #save data

    save_data(data)

    return JSONResponse(status_code=200, content={"message":"patient updated"})



# DELETE
# delete endpoint to delete any patient data
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    #load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='patient not found')
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message":"patient deleted successfully"})