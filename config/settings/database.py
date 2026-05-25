from config.settings.env import (
    BASE_DIR,
    DATABASE_ENGINE,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

if DATABASE_ENGINE == "django.db.backends.postgresql":
    DATABASES = {
        "default": {
            "ENGINE": DATABASE_ENGINE,
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
