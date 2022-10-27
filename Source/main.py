import primePy.primes
from fastapi import FastAPI, File, Header, Response
import ctypes
from PIL import Image
import PIL.ImageOps
import io
from fastapi.responses import StreamingResponse
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime
import uvicorn

from os import environ

fake_users_db = {
    "pmika": {
        "username": "pmika",
        "hashed_password": "$2b$12$MZcgYluT8Z6Xswzr6DJnL.lxER6wzm9AiBlA6wYtRMm1.8vxZ9Xym"  # password: !QAZxsw2
    }
}


class UserInDB(BaseModel):
    username: str
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str) -> UserInDB:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str) -> bool:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True


primeLib = ctypes.CDLL('./libprime.so')
primeLib.isPrime.restype = ctypes.c_bool
primeLib.isPrime.argtypes = [ctypes.c_ulonglong]

app = FastAPI()


@app.get("/")
async def homePage():
    return Response(content="<h2>Witaj, lista dostępnych endpointów jest tutaj: "
                            "<a href=\"https://superapi-pmika.herokuapp.com/docs\">"
                            "https://superapi-pmika.herokuapp.com/docs/<a></h2>", media_type="text/html")


@app.get("/prime/{number}")
async def isPrime(number):
    if number.isnumeric() and len(number) < 20:
        number = int(number)
        if number == 0 or number == 1:
            return False
        elif number == 2:
            return True
        temp = primeLib.isPrime(number)
        return temp
    else:
        return {"Argument nie jest liczbą naturalną"}


@app.post("/picture/invert")
async def getInvertedImage(file: bytes = File()):
    image = Image.open(io.BytesIO(file))
    inverted_image = PIL.ImageOps.invert(image)
    responseImage = io.BytesIO()
    inverted_image.save(responseImage, "JPEG")
    responseImage.seek(0)
    return StreamingResponse(responseImage, media_type="image/jpeg")


@app.get("/get-time")
async def getTime(username: str | None = Header(default=None), password: str | None = Header(default=None)):
    if authenticate_user(fake_users_db, username, password):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return {current_time}
    else:
        return {"Niepoprawne dane autoryzacyjne"}


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=environ.get("PORT", 5000))
