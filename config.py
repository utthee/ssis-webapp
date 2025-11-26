from os import getenv

SECRET_KEY = getenv("SECRET_KEY")

DB_NAME = getenv("DB_NAME")
DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT", "5432")
DATABASE_URI = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USERNAME} password={DB_PASSWORD}"

SUPABASE_URL = getenv("SUPABASE_DB_URL")
SUPABASE_KEY = getenv("SUPABASE_SERVICE_KEY")

DEFAULT_PROFILE_URL = getenv("DEFAULT_PROFILE_URL")