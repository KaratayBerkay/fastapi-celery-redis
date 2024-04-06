import os


class Config:
    TITLE = "API Service"
    DESCRIPTION = "This api is serves Crud only."
    INSECURE_PATHS = [
        "/",
        "/openapi.json",
        "/openapi.json_files",
        "/docs",
        "/redoc",
        "/favicon.ico",
        "/docs/oauth2-redirect",
        "/authentication/login",
        "/authentication/logout",
    ]
    SECRET_KEY = os.getenv("SECRET_KEY", "")

