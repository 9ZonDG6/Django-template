from split_settings.tools import include

include(
    "env.py",
    "django.py",
    "apps.py",
    "database.py",
    "rest_framework.py",
    "silk.py",
    "axes.py",
    "extra_checks.py",
    "zeal.py",
    scope=globals(),
)
