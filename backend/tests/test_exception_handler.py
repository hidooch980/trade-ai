from app.core.errors.exception_handler import ExceptionHandler


handler = ExceptionHandler()


try:

    value = 10 / 0


except Exception as e:

    result = handler.handle(
        e,
        context="TRADING_PIPELINE"
    )


print("EXCEPTION RESULT:")
print(result)
