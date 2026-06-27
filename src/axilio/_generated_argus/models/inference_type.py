from enum import Enum


class InferenceType(str, Enum):
    COMBINED = "combined"
    OCR = "ocr"
    YOLO = "yolo"

    def __str__(self) -> str:
        return str(self.value)
