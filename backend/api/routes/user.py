import datetime

from fastapi import APIRouter, Depends, UploadFile, Form
from schemas.time_capsule import TimeCapsuleBase
from schemas.user import UserBase
from typing import List, Optional
from secrets import token_hex
from utils.token import decode_token, encode_token
from utils.password_hashing import get_password_hash
from db.db_conn import users_collection, time_capsules_collection #THIS WILL BE MOVED TO CRUD
from typing_extensions import Annotated
from datetime import date
import uuid
import os

router = APIRouter(prefix="/user",
                   tags=['user'])

# Directory to save uploaded files
UPLOAD_DIRECTORY = "uploads"

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)



@router.get(path="/{userid}/time-capsules")
def get_user_time_capsules():
    pass

@router.get(path="/{userid}/time-capsules/{timecapsuleid}")
def get_user_time_capsule(payload = Depends(decode_token)):
    return payload

@router.post(path="/create-user")
def create_new_user(user:UserBase):
    user_doc = dict(user)
    #verify if no duplicate users
    user_doc['hash_password'] = get_password_hash(user_doc['password'])
    del user_doc['password']
    resp = users_collection.insert_one(user_doc) #MOVE TO CRUD

    return {
        "status": "ok",
        "message": f"added {user_doc['email']} to db"
    }

@router.post(path="/create-time-capsule")
async def create_time_capsule(time_capsule_name:Annotated[str, Form()],
                            target_date:Annotated[date, Form()],
                            is_public: Annotated[bool, Form()],
                            notes: Annotated[List[str], Form()],
                            files: List[UploadFile],
                            payload = Depends(decode_token)):
    user = payload.get("sub")
    file_path = None
    if files:
        file_path = f"{UPLOAD_DIRECTORY}/timecapsule_{user}_{uuid.uuid1()}/"
        os.makedirs(file_path)
        for file in files:
            file_ext = file.filename.split(".").pop()
            file_name = f"{token_hex(10)}.{file_ext}"
            #file_path = f"{UPLOAD_DIRECTORY}/timecapsule_{user}_{uuid.uuid1()}/{file_name}.{file_ext}"

            with open(file_path + file_name, "wb") as f:
                content = await file.read()
                f.write(content)

    time_capsule_doc = {
        "owner": user,
        "time_capsule_name": time_capsule_name,
        "target_date":  datetime.datetime.combine(target_date, datetime.time()),
        "is_public": is_public,
        "notes": [note for note in notes],
        "files": file_path
    }

    resp = time_capsules_collection.insert_one(time_capsule_doc)
    return {
        "status": "ok",
        "message": f"added {time_capsule_name} to db"
    }
"""
@router.post(path="/create-time-capsule")
async def create_time_capsule(time_capsule_base:TimeCapsuleBase,files: List[UploadFile], decoded_token = Depends(decode_token)):
    uploaded_files = []
    for file in files:
        file_ext = file.filename.split(".").pop()
        file_name = token_hex(10)
        file_path = f"{UPLOAD_DIRECTORY}/{file_name}.{file_ext}"

        with open(file_path, "wb") as f:
            content = await  file.read()
            f.write(content)
        uploaded_files.append(file_path)

    return {"filenames": uploaded_files, "time_capsule":time_capsule_base}
"""
"""
@router.post(path="/create-time-capsule")
async def create_time_capsule(files: List[UploadFile], decoded_token = Depends(decode_token)):
    user = decoded_token.get("sub")
    for file in files:
        file_ext = file.filename.split(".").pop()
        file_name = token_hex(10)
        path_name =
    insert_time_capsule(db,timecapsuledata)
    return {"filenames": [file.filename for file in files]}
"""