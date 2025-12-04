import os

DB_HOST: str = "localhost"
DB_PORT: int = 5432
DB_NAME: str = "teachers_db"
DB_USER: str = "postgres"
DB_PASSWORD: str = "1234"

DATA_DIR: str = os.path.join(os.path.dirname(__file__), "data")
JSON_FILENAME: str = os.path.join(DATA_DIR, "teachers.json")
YAML_FILENAME: str = os.path.join(DATA_DIR, "teachers.yaml")

REPOSITORY_TYPE: str = "json"
ITEMS_PER_PAGE: int = 10
