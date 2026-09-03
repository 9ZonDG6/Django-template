from config.settings.env import LOGGING_ENABLED, ZEAL_ENABLED

if ZEAL_ENABLED:
    globals()["INSTALLED_APPS"].append("zeal")
    globals()["MIDDLEWARE"].insert(2, "zeal.middleware.zeal_middleware")

    ZEAL_RAISE = False

    if LOGGING_ENABLED:
        globals()["LOGGING"]["loggers"]["py.warnings"]["handlers"].append("zeal_file")
