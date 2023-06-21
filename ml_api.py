# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 17:01:23 2022

@author: User
"""

from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
import numpy as np

from fastapi.middleware.cors import CORSMiddleware
import pandas as pd



    
    
#app = FastAPI()
app = FastAPI()
origins = [
  

    "http://localhost",
    "http://localhost:3000",
    "http://localhost:4000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):
    
    product_name: str
        
        
# loading the saved model
model = pickle.load(open('model.sav', 'rb'))

product_pivot = pickle.load(open('product_pivot.sav', 'rb'))
product_data = pickle.load(open('product_data.sav', 'rb'))


@app.post('/products_prediction')

def products_predd(input_parameters : model_input):
    list1=[]
    list2=[]
    #title = []
    
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    
    prod = input_dictionary['product_name']
    input_list = prod
    
    
    
  
    product_id = np.where(product_pivot.index == input_list)[0][0]
    distances, suggestions =model.kneighbors(product_pivot.iloc[product_id, :].values.reshape(1,-1), n_neighbors =6)
    #for i in range(len(suggestions)):
    for x in range(5):
     d = product_data[product_data.name ==product_pivot.index[suggestions[0][x]]].to_dict(orient='record')
   #  if product_pivot.index[suggestions[0][x]] not in title:
     list1.extend(d)
   


     # title.extend(product_pivot.index[suggestions[0][x]])
   
    
    list2 =  pd.DataFrame(list1).drop_duplicates('name').to_dict(orient='records')
    print(list2) 
    return list2
   
    
    
    
   
   # prediction = diabetes_model.predict([input_list])
    
  #  if (prediction[0] == 0):
    #    return 'The person is not diabetic'
 #   else:
   
    
    
