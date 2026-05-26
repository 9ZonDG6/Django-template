from config.settings.env import ZEAL_ENABLED

if ZEAL_ENABLED:
    globals()["INSTALLED_APPS"].append("zeal")
    globals()["MIDDLEWARE"].insert(2, "zeal.middleware.zeal_middleware")

    ZEAL_RAISE = False
