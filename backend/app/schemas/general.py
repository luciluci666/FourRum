from pydantic import BaseModel

from . import RegForm


class Token(BaseModel):
    access_token: str
    token_type: str

class BasicResponse(BaseModel):
    detail: str
    status_code: int

class RegResponse(BaseModel):
    detail: str
    reg_data: RegForm



