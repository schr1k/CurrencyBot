from pydantic_settings import BaseSettings


class Config(BaseSettings):
    TOKEN: str
    API_KEY: str

    class Config:
        env_file = '.env'


config = Config()
