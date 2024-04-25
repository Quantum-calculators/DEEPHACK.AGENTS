from pydantic import BaseModel
from datetime import datetime


class RequestStatHypothesis(BaseModel):
    UUID: str
    userData: str
    error: str


class Style(BaseModel):
    Color: str | None = "blue"
    plotSize: int | None = 10


class PlotData(BaseModel):
    X: list[float] | None = []
    Y: list[float] | None = []
    Z: list[float] | None = []
    style: Style


class ResponseStatHypothesis(BaseModel):
    UUID: str
    gigachainData: str | None = None
    plotType: str | None = None
    plotData: PlotData | None = None
    error: str


class Message(BaseModel):
    text: str
    plotType: str | None = None
    plotData: PlotData


class ResponseMessage(BaseModel):
    user: bool
    UUID: str
    date: datetime
    message: Message
    error: str
