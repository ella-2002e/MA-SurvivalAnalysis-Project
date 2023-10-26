import uvicorn
import os
import fastapi

from survival_analysis.api import app

if __name__== "__main__":
    uvicorn.run(app, reload = True)