import os

database_config = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASS", "postgres"),
    "database": os.getenv("DB_NAME", "postgres"),
    "port": os.getenv("DB_PORT", "5432"),
}


def build_database_url():
    return f"postgresql://{database_config['user']}:{database_config['password']}@{database_config['host']}:{database_config['port']}/{database_config['database']}"
