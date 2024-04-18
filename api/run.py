""" This module contains the FastAPI application that serves the API endpoints. """

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src import ScanPhoto, getText

app = FastAPI()
scaner = ScanPhoto()


@app.post("/scan_photo", status_code=200)
async def scan_photo(photo: UploadFile):
    """
    Endpoint for scanning a photo.
    Takes an uploaded photo file as input.
    Returns a JSON response with the detected objects in the photo and the extracted text and audio.
    """
    get_object = await scaner.scan_photo(photo)

    if get_object["objects"] == []:
        raise HTTPException(status_code=404, detail="Object not found")

    get_text_and_audio = await getText(get_object["objects"][0])  # type: ignore

    return get_object | get_text_and_audio  # type: ignore


class GetMedia(BaseModel):
    path: str


@app.post("/get_media", status_code=200)
async def get_media(data: GetMedia):
    """
    Endpoint for retrieving media files.
    Takes a path to a media file as input.
    Returns the media file as a response based on the file type (image or audio).
    """
    if data.path.split("/")[0] == "media":
        return FileResponse(data.path, media_type="image/jpeg")
    if data.path.split("/")[0] == "audio":
        return FileResponse(data.path, media_type="audio/mpeg")
