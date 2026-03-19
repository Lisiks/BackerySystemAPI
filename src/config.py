from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int

    SERVER_HOST: str
    SERVER_PORT: int

    DIRECTORY_NAME: str = "src"
    PRODUCT_IMAGE_DIR: str = "src/static/products"

    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: list = ["GET", "POST", "PUT"]
    CORS_ALLOW_HEADERS: list = ["*"]

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_link(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def full_domain(self):
        return f"http://{self.SERVER_HOST}:{self.SERVER_PORT}/"

settings = Settings()
