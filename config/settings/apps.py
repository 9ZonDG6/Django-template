LOCAL_APPS = []

THIRD_PARTY_APPS = [
    "axes",
    "extra_checks",
    "rest_framework",
    "corsheaders",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]
