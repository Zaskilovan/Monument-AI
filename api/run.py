from fastapi import FastAPI, UploadFile , Query, HTTPException , Body
from fastapi.responses import FileResponse
from typing import Optional
from src import ScanPhoto , getText # type: ignore
from pydantic import BaseModel

app = FastAPI()
scaner = ScanPhoto()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/scan_photo", status_code=200)
async def scan_photo(
    photo: UploadFile,
    longitude: Optional[float] = Query(None, title="Longitude", description="Longitude of the photo", ge=-180, le=180), 
    latitude: Optional[float] = Query(None, title="Latitude", description="Latitude of the photo", ge=-90, le=90),
    ):

              
    get_object =  await scaner.scan_photo(photo, longitude, latitude)

    if get_object['objects'] == []:
        raise HTTPException(status_code=404, detail="Object not found")
    
    get_text_and_audio = await getText(get_object['objects'][0]) # type: ignore
    print(get_object)
    # get_text_and_audio = {}
    return get_object | get_text_and_audio # type: ignore
    
class GetMedia(BaseModel):
    path: str



@app.post("/get_media", status_code=200)
async def get_media(data: GetMedia):
    if data.path.split('/')[0] == 'media':
        return FileResponse(data.path, media_type="image/jpeg")
    if data.path.split('/')[0] == 'audio':
        return FileResponse(data.path, media_type="audio/mpeg")

    

