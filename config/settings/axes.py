from datetime import timedelta

from config.settings.env import AXES_COOLOFF_MINUTES, AXES_ENABLED, AXES_FAILURE_TRIES

if AXES_ENABLED:
    AXES_FAILURE_LIMIT = AXES_FAILURE_TRIES
    AXES_COOLOFF_TIME = timedelta(minutes=AXES_COOLOFF_MINUTES)

    AXES_LOCK_OUT_AT_FAILURE = True
    AXES_RESET_ON_SUCCESS = True

    AXES_USE_ATTEMPT_EXPIRATION = True
    AXES_HTTP_RESPONSE_CODE = 429

    AXES_LOCKOUT_PARAMETERS = ["ip_address", ["username", "user_agent"]]
