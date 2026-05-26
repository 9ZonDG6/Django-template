from config.settings.env import DEBUG

if DEBUG:
    globals()["INSTALLED_APPS"].append("zeal")
    globals()["MIDDLEWARE"].insert(2, "zeal.middleware.zeal_middleware")

    ZEAL_RAISE = False
