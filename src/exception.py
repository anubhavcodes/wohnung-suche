class Error(Exception):
    pass


class EnvironmentVariableError(Error):
    pass


class ConfigurationError(Error):
    pass


class CardNotFoundException(Error):
    pass
