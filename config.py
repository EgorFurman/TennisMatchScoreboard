import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self, driver: str, user: str, password: str, host: str, port: str, database: str) -> None:
        self.driver = driver
        self.user = user
        self.password = password
        self.host = host
        self.port = int(port)
        self.database = database

    @property
    def CONNECTION_URL(self):
        return f'{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'


settings = Settings(
    driver=os.getenv("DB_DRIVER"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
)