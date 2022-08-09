



from pydantic import BaseSettings


class Settings(BaseSettings):
    my_secret : str

    class Config:
        env_file : str = ".env"



def get_settings( settings = Settings() ) -> Settings:
    return settings

