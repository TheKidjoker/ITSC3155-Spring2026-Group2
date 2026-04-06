import os

class conf:
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "sandwich_maker_api")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    app_host = os.getenv("APP_HOST", "localhost")
    app_port = int(os.getenv("APP_PORT", "8000"))