from pydantic import BaseModel, model_validator
from datetime import date
from typing import List, Optional
from fastapi import UploadFile
import json

class TimeCapsuleBase(BaseModel):
    time_capsule_name: str
    target_date: date
    is_public: bool
    texts: Optional[List[str]] = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class TimeCapsule(TimeCapsuleBase):
    files: Optional[List[str]] = None