
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .Route.UserRoute import UserRouter

app = FastAPI(
    version= "0.0.1",
    title= "Coffee Shop API",
    default_response_class= ORJSONResponse
)

app.include_router(UserRouter)


