from pydantic import BaseModel


class UserResponse(BaseModel):
    ok       : bool
    msg      : str
    username : str
    token    : str|None

    def __init__(self, ok:bool , msg:str, token:str|None ):
        self.ok    = ok
        self.msg   = msg
        self.token = token


class UserPostBody(BaseModel):
    phone    : str
    password : str

class NewUserPostBody(UserPostBody):
    username : str


class RenewBody(UserPostBody):
    token : str




