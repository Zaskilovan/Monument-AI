from fastapi import FastAPI, UploadFile , Query
from typing import Optional
from src import Scaner

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/scan_photo", status_code=200)
async def scan_photo(
    photo: UploadFile,
    longitude: Optional[float] = Query(None, title="Longitude", description="Longitude of the photo", ge=-180, le=180), 
    latitude: Optional[float] = Query(None, title="Latitude", description="Latitude of the photo", ge=-90, le=90),
    ):

    print(1)                 
    return await Scaner.scan_photo(photo, longitude, latitude)





