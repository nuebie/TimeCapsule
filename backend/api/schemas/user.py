from pydantic import BaseModel, model_validator
from datetime import date
from typing import List, Optional
from fastapi import UploadFile
import json

class UserBase(BaseModel):
    email: str
    password: str