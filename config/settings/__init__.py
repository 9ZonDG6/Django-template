from split_settings.tools import include

include(
    "env.py",
    "django.py",
    "apps.py",
    "database.py",
    "silk.py",
    "axes.py",
    "extra_checks.py",
    scope=globals(),
)
