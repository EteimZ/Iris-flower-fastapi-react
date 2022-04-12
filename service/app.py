import uvicorn
from pydantic import BaseModel, Field

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from joblib import load
import numpy as np


app = FastAPI(title="Iris flower predictor", description="API to predict the species of an Iris flower.")

class Iris(BaseModel):
    sepalLength: float = Field(..., description="The length of the sepal.")
    sepalWidth: float = Field(..., description="The width of the sepal.")
    petalLength: float = Field(..., description="The length of the petal.")
    petalWidth: float = Field(..., description="The width of the petal.")

classifier = load('./classifier.joblib')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/prediction')
def predict(iris: Iris):
    try:
        data = [val for val in iris.dict().values()]
        prediction = classifier.predict(np.array(data).reshape(1, -1))
        types = { 0: "Iris Setosa", 1: "Iris Versicolour ", 2: "Iris Virginica"}
        response = {
                    "statusCode": 200,
                    "status": "Prediction made",
                    "result": "The type of iris plant is: " + types[prediction[0]]
                    }
        return response
    except Exception as e:
        response = {
                    "statusCode": 500,
                    "status": "Prediction failed",
                    "result": "The prediction failed with the following error: " + str(e)
                    }
        return response
    

if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0.', port=8000, reload=True)