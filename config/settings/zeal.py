from config.settings.env import LOGGING_ENABLED, ZEAL_ENABLED

if ZEAL_ENABLED:
    globals()["INSTALLED_APPS"].append("zeal")

    middleware: list[str] = globals()["MIDDLEWARE"]
    # Сразу после SilkyMiddleware, если он включён (см. silk.py), иначе — сразу после
    # SecurityMiddleware. У zeal нет требований к порядку, в отличие от silk.
    anchor = (
        "silk.middleware.SilkyMiddleware"
        if "silk.middleware.SilkyMiddleware" in middleware
        else "django.middleware.security.SecurityMiddleware"
    )
    middleware.insert(middleware.index(anchor) + 1, "zeal.middleware.zeal_middleware")

    ZEAL_RAISE = False

    if LOGGING_ENABLED:
        globals()["LOGGING"]["loggers"]["py.warnings"]["handlers"].append("zeal_file")
