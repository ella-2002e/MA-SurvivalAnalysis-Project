#Importing libraries
import uvicorn
import os
import fastapi

from survival_analysis.api import app

if __name__== "__main__":
    uvicorn.run(app)

# if __name__ == "__main__":
#     uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True)

