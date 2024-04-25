from typing import Annotated
from fastapi import APIRouter, status, Cookie
from Name.schemas import (
    RequestStatHypothesis,
    ResponseStatHypothesis,
    PlotData,
    Style,
    ResponseMessage,
)
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import aiohttp
from datetime import datetime

import uuid
import json

from database import client

route = APIRouter(prefix="/Name", tags=["Name"])

auth_data = "Yjg4MTQzMmUtNDAwMS00NDk0LThjOGUtNmU5ZWQ2YzQ4NDQ2OmQ4MWMxZGZiLTFmNGYtNDk5NS05OGQzLTBiMzYyYWJmNjk3OA=="


@route.get(
    "/message_api",
    status_code=status.HTTP_200_OK,
)
async def message(UUID: str | None = None):
    MessageDB = client["MessageDB"]
    UserDB = client["UserDB"]
    if UUID:
        result = MessageDB.find({"UUID": UUID}, {"_id": 0})
        messages = []
        async for elem in result:
            messages.append(elem)
        print(messages)
        return {"result": messages}
    return {"result": []}


@route.post(
    "/add_user",
    status_code=status.HTTP_201_CREATED,
)
async def addUser():
    UserDB = client["UserDB"]
    userUUID = str(uuid.uuid4())
    access_token = ""
    expires_at = ""
    try:
        access_token, expires_at = await authGigaChat(userUUID=userUUID)
        UserDB.insert_one(
            {"UUID": userUUID, "access_token": access_token, "expires_at": expires_at}
        )
        return JSONResponse({"UUID": userUUID, "error": ""})
    except Exception as e:
        print(userUUID, e)
        UserDB.insert_one({"UUID": userUUID, "access_token": "", "expires_at": ""})
        return JSONResponse({"UUID": userUUID, "error": str(e)})


@route.post(
    "/stat_hypothesis_api",
    response_model=ResponseStatHypothesis,
    status_code=status.HTTP_200_OK,
)
async def statHypothesis(
    request: RequestStatHypothesis,
):
    # Client = client["client"]
    MessageDB = client["MessageDB"]
    UserDB = client["UserDB"]
    resp = ResponseStatHypothesis(UUID="", error="")

    # проверка на нового пользователя
    if request.UUID:
        resp.UUID = request.UUID
    else:
        resp.error = "Пользователя не существует. Перед вызовом /stat_hypothesis_api выполните выхов /add_user"
        return resp
    MessageDB.insert_one(
        {
            "user": True,
            "UUID": resp.UUID,
            "date": datetime.now(),
            "Message": {
                "text": request.userData,
                "PlotType": None,
                "PlotData": {
                    "X": None,
                    "Y": None,
                    "Z": None,
                    "Styles": {
                        "Color": None,
                        "PlotSize": None,
                    },
                },
            },
            "Error": None,
        }
    )
    userData = await UserDB.find_one({"UUID": request.UUID})
    access_token = userData["token"]
    expires_at = userData["expires_at"]

    # проверка не истек ли токен
    if datetime.fromtimestamp(expires_at) < datetime.now():
        try:
            access_token, expires_at = await authGigaChat(userUUID=resp.UUID)
            UserDB.update_one(
                {"UUID": resp.UUID},
                {"access_token": access_token, "expires_at": expires_at},
            )
        except Exception as e:
            print(resp.UUID, e)
            resp.error = str(e)
            return resp

    # делаем запрос к gigachain для расчета статистики.
    try:
        data = await getGigachainDataMock(request.userData)
        resp.gigachainData = data[
            "gigachainData"
        ]  # Если получиться сделать формат ответа JSON, то можно просто никак не форматируя отправлять его на фронт
        resp.plotType = data["plotType"]
        resp.plotData = PlotData(
            X=data["X"],
            Y=data["Y"],
            Z=data["Z"],
            style=Style(Color=data["color"], plotSize=data["plotSize"]),
        )
        resp.error = ""
        MessageDB.insert_one(
            {
                "user": False,
                "UUID": resp.UUID,
                "date": datetime.now(),
                "Message": {
                    "text": resp.gigachainData,
                    "PlotType": resp.plotType,
                    "PlotData": {
                        "X": resp.plotData.X,
                        "Y": resp.plotData.Y,
                        "Z": resp.plotData.Z,
                        "Styles": {
                            "Color": resp.plotData.style.Color,
                            "PlotSize": resp.plotData.style.plotSize,
                        },
                    },
                },
                "Error": resp.error,
            }
        )
        return resp
    except Exception as e:
        print(resp.UUID, e)
        resp.error = "Не удалось обработать запрос"
        return resp


# TODO: реализовать выполнение запроса
async def getGigachainDataMock(userMessage: str) -> dict[str]:
    return {
        "gigachainData": "Для проверки гипотезы о равенстве средних значений двух \
выборок можно воспользоваться t-тестом для независимых выборок. В данном \
случае, нулевая гипотеза будет состоять в том, что средние значения \
для обеих выборок равны. Давайте проведем данное тестирование. Сначала, \
давайте посчитаем средние значения для каждой выборки. Для выборок:",
        "plotType": "Norm",
        "X": [1.2],
        "Y": [0.2],
        "Z": [],
        "color": "blue",
        "plotSize": 10,
    }


async def authGigaChat(userUUID: str) -> tuple[str, str]:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = "scope=GIGACHAT_API_CORP"
    async with aiohttp.ClientSession() as session:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(userUUID),
            "Authorization": f"Basic {auth_data}",
        }
        userData = await session.post(url=url, headers=headers, data=payload, ssl=False)
        if userData.status != 200:
            raise Exception("Не удалось получить токен доступа к GigiChat")

        jsonUserData = await userData.json()
        return (jsonUserData["access_token"], jsonUserData["expires_at"])
