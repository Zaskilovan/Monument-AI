import os
from fastapi import UploadFile
from typing import Optional
from base64 import b64encode

from fastapi.responses import FileResponse

import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
import pprint

from uuid import uuid4

objects = {
    "Opera theatre" : { 
        "latitude" : 46.485058,
        "longitude" : 30.741136,
    },
    "The Potemkin Stairs":{
        "latitude" : 46.488868,
        "longitude" : 30.742358,
    }
}, 


class ScanPhoto:

    def __init__(self):
        self.model = YOLO("weights/best.pt")
        self.box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=2,
            text_scale=1 )
    
    async def scan_photo(self, photo: UploadFile, longitude: Optional[float], latitude: Optional[float]):

        # Read the photo
        contents = await photo.read()

        # Преобразуем массив байтов в массив numpy
        nparr = np.frombuffer(contents, np.uint8)

        # Декодируем массив numpy в кадр OpenCV
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = self.model(frame, agnostic_nms=True)[0]


        detections = sv.Detections.from_ultralytics(result)
        labels = [
            f"{self.model.model.names[class_id]} {confidence:0.2f}"  # type: ignore
            for _, _, confidence, class_id, *_
            in detections
        ]


        frame = self.box_annotator.annotate(
                        scene=frame, 
                        detections=detections, 
                        labels=labels
                    )
        
        os.makedirs('media', exist_ok=True)
        path = f"media/{uuid4()}.jpg"
        cv2.imwrite(path, frame)

        return {"photo_path": path, "objects": labels}

        # return FileResponse(path, media_type="image/jpeg")
    






