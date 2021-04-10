from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from base64 import b64encode, b64decode
import os


class Base64FileInput(BaseModel):
    uid: str
    filename: str
    b64_file: str
    userName: str


api = FastAPI()

#api to upload data

@api.put('/upload')
async def get_file(_file: Base64FileInput):
    try:
        file_content = b64decode(_file.b64_file)
    except:
        raise HTTPException(
                status_code=500,
                detail="Invlid Base64 supplied."
                )
    with open(f'files/{_file.userName}/{_file.uid}/{_file.filename}', 'wb') as __file:
        __file.write(file_content)
    return {
            "user_id": _file.uid,
            "operation": "success"
            }

class UserModel(BaseModel):
    uid: str
    userName: str

# api to read all the data
@api.put('/createuser')
async def create_user(_user: UserModel):
    try:
        _path = f'files/{_user.userName}/{_user.uid}' 
        #_user.uid+"/"+_user.userName
        if not os.path.exists(_path):
            os.makedirs(_path)
            return {
                "operation": "success",
                "message": "dir created for the user"
                    }
        else:
            return {
                    "message": "user already exist?",
                    "operation": "error"
                    }
    except Exception as e:
        print(e)
        raise HTTPException(
                status_code=400,
                detail="Some error occured"
                )
