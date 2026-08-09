from datetime import datetime, timedelta, timezone


MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


def is_account_locked(user) -> bool:
    if user.locked_until is None:
        return False

    return user.locked_until > datetime.now(timezone.utc)


def register_failed_login(user) -> bool:
    user.failed_login_attempts += 1

    if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
        user.locked_until = (
            datetime.now(timezone.utc)
            + timedelta(minutes=LOCKOUT_MINUTES)
        )
        return True

    return False


def reset_failed_logins(user) -> None:
    user.failed_login_attempts = 0
    user.locked_until = None
