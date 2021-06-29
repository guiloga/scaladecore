class EntityFactoryError(Exception):
    def _init__(self, entity_type: str):
        self.entity_type = entity_type

    def __str_(self):
        return f'"{self.entity_type}" is not a valid entity type.'


class BearerTokenParseError(Exception):
    def __str__(self):
        return "Unable to parse Bearer Token: failed matching regular expression."


class BaseContextError(Exception):
    def __init__(self, error_payload: dict = None):
        self._error_payload = error_payload

    def __str__(self):
        if self._error_payload:
            return "%s" % self._error_payload
        else:
            return ""


class ContextInitError(BaseContextError):
    def __str__(self):
        return ("Unable to initialize properly the ContextManager object. " +
                super().__str__())


class ContextLogError(BaseContextError):
    def __str__(self):
        return ("An error occurred while creating a log message. " +
                super().__str__())


class ContextBlockError(BaseContextError):
    def __str__(self):
        return ("An error occurred on block function instance. " +
                super().__str__())


class ContextCompleteError(BaseContextError):
    def __str__(self):
        return ("An error occurred on complete function instance. " +
                super().__str__())


class ContextOutputError(BaseContextError):
    def __str__(self):
        return ("An error occurred while creating an output. " +
                super().__str__())
