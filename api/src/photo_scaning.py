""" This module is responsible for scanning a photo for objects and returning the annotated image path and detected objects."""

import os
from uuid import uuid4

import cv2
import numpy as np
import supervision as sv  # type: ignore
from fastapi import UploadFile
from ultralytics import YOLO  # type: ignore


class ScanPhoto:
    """
    Class representing a photo scanning object.

    Attributes:
        model (YOLO): The YOLO model used for object detection.
        box_annotator (BoxAnnotator): The box annotator used for drawing bounding boxes on the image.

    Methods:
        scan_photo: Scans a given photo for objects and returns the annotated image path and detected objects.
    """

    def __init__(self):
        self.model = YOLO("weights/best (17).pt")
        self.box_annotator = sv.BoxAnnotator(
            thickness=2, text_thickness=2, text_scale=1
        )

    async def scan_photo(self, photo: UploadFile):
        """
        Scans a given photo for objects and returns the annotated image path and detected objects.

        Args:
            photo (UploadFile): The photo to be scanned.

        Returns:
            dict: A dictionary containing the annotated image path and detected objects.
        """
        # Read the photo
        contents = await photo.read()

        # Преобразуем массив байтов в массив numpy
        nparr = np.frombuffer(contents, np.uint8)

        # Декодируем массив numpy в кадр OpenCV
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = self.model(frame, agnostic_nms=True)[0]

        detections = sv.Detections.from_ultralytics(result)

        labels = []
        for _, _, confidence, class_id, *_ in detections:
            if confidence > 0.6:  # type: ignore
                if class_id in [1, 2]:  # Оперные театр и Потемкинская лестница
                    labels.append(f"{self.model.model.names[class_id]} {confidence:0.2f}")  # type: ignore

        frame = self.box_annotator.annotate(
            scene=frame, detections=detections, labels=labels
        )

        os.makedirs("media", exist_ok=True)
        path = f"media/{uuid4()}.jpg"
        cv2.imwrite(path, frame)

        return {"photo_path": path, "objects": labels}
