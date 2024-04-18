from pydantic import BaseModel


class RequestText(BaseModel):
    text: str

class ResponseText(BaseModel):
    text: str