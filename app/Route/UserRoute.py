import jwt

from fastapi.responses import ORJSONResponse
from fastapi import APIRouter, Header, Response, status
from app.auth.Auth import AuthService
from app.dependencies.PhoneValidator import validate_phone

from app.env.Env import Settings, get_settings
from app.locadata.LocalData import LocalDB, get_db_instance
from app.models import UserResponse, UserPostBody, NewUserPostBody


UserRouter = APIRouter(
    prefix= "/user",
)

settings: Settings = get_settings()
database: LocalDB  = get_db_instance()

# --- NEW USER ENDPOINT ---
@UserRouter.post("/new", response_model= UserResponse)
async def create_new_user(body : NewUserPostBody, res : Response):

    isValidPhone = validate_phone(body.phone)
    if not isValidPhone:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return ORJSONResponse({
            "ok"    : False,
            "msg"   : "Unvalid Phone Number, must be (000)0000-0000",
            "username" : "NO USER",
            "token" : None
        })

    result = database.get_user_from_db( phone= body.phone)
    if(result != None):
        res.status_code = status.HTTP_400_BAD_REQUEST
        return ORJSONResponse({
            "ok"       : False,
            "msg"      : "User Already Exist",
            "username" : "Already Exist",
            "token"    : None
        })

    encrypted_pass:str = AuthService.encrypt_password(body.password)
    user_id:int = database.create_user(
        name     = body.username,
        phone    = body.phone,
        password = encrypted_pass)

    payload_token = {"userId" : str(user_id), "username" : body.username}
    token = AuthService.generate_jwt( payload= payload_token )

    return ORJSONResponse({
        "ok"       : True,
        "msg"      : "You're registered",
        "username" : body.username,
        "token"    : token
    })


# --- LOGIN ENDPOINT --- 
@UserRouter.post("/login", response_model= UserResponse)
async def login_user(body : UserPostBody, res : Response):
    

    result = database.get_user_from_db( body.phone )
    if result == None:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return ORJSONResponse({
            "ok"    : False,
            "msg"   : "Invalid Credentials",
            "username" : "NO USER",
            "token" : None
        })
    
    isValidatePass = AuthService.validate_password(body.password , result[3])
    if not isValidatePass:
        return ORJSONResponse({
            "ok"    : False,
            "msg"   : "Invalid Credentials",
            "username" : "NO USER",
            "token" : None
        })
    
    payload_token = { "userId" : result[0] , "username" : result[1]}
    token = AuthService.generate_jwt( payload= payload_token )

    return ORJSONResponse({
        "ok"    : True,
        "msg"   : "User logged",
        "username" : result[1],
        "token" : token 
    })
    
# --- RENEW TOKEN ---   
@UserRouter.post("/renew" , response_model= UserResponse)
async def renew_token( res : Response , x_token:str|None = Header(None)):
    if x_token == None:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return ORJSONResponse({
            "ok"   : False,
            "msg"  : "No Token",
            "username" : "NO USER",
            "token": None
        })
    
    try:
        token_payload = jwt.decode(x_token, settings.my_secret, ["HS256"])
        user_db = database.get_user_by_id(token_payload["userId"])
        if user_db == None:
            res.status_code = status.HTTP_400_BAD_REQUEST
            return ORJSONResponse({
            "ok"   : False,
            "msg"  : "No USER",
            "username" : "NO USER",
            "token": None
        })

        new_payload = { "userId" : user_db[0] , "username" : user_db[1] } 
        new_token   = AuthService.generate_jwt(new_payload)

        return ORJSONResponse({
            "ok"   : True,
            "msg"  : "Token Remade",
            "username" : user_db[1],
            "token": new_token
        })

    except:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return ORJSONResponse({
            "ok"   : False,
            "msg"  : "INVALID TOKEN",
            "username" : "NO USER",
            "token": None
        })

