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

    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: list = ["GET", "POST", "PUT", "DELETE"]
    CORS_ALLOW_HEADERS: list = ["*"]

    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REFRESH_COOKIE_NAME: str = "refresh_token"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    SMTP_SERVER: str
    SMTP_PORT: int
    SUPPORT_EMAIL_ADDRESS: str
    SUPPORT_EMAIL_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_link(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def full_domain(self):
        return f"http://{self.SERVER_HOST}:{self.SERVER_PORT}/"

    @property
    def CORS_ORIGINS(self):
        return [f"{self.SERVER_HOST}:{self.SERVER_PORT}"]

settings = Settings()
