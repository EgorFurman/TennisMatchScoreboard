class TennisScoreboardError(Exception):
    """Base class for exceptions in this project."""
    def __init__(self, *args):
        self.message = f'Base tennis scoreboard exception'

    def __str__(self):
        return self.message


class MethodNotAllowed(TennisScoreboardError):
    def __init__(self, method, *args):
        self.message = f'Method {method} not allowed'


class PathNotFoundError(TennisScoreboardError):
    """Exception raised when a requested URL is not found."""

    def __init__(self, path, *args):
        self.message = f'Requested path "{path}" not found'


class PlayerAlreadyExistsError(TennisScoreboardError):
    """Exception raised when trying to create already exists player."""
    def __init__(self, name, *args):
        self.message = f'Player "{name}" already exists'


class PlayerNotFoundError(TennisScoreboardError):
    """Exception raised when player not found."""

    def __init__(self, name, *args):
        self.message = f'Player with name: "{name}" not found'


class MatchNotFoundError(TennisScoreboardError):
    """Exception raised when match not found."""

    def __init__(self, uuid: str, *args):
        self.message = f'Match with UUID "{uuid}" not found'


class MissingRequestHeadersError(TennisScoreboardError):
    """Exception raised when missing at least one request headers."""
    def __init__(self, *args):
        self.message = f'Missing at least one request headers: {", ".join(*args)}'


class MissingRequestFieldsError(TennisScoreboardError):
    """Exception raised for a request with missing form fields."""
    def __init__(self, *args):
        self.message = f'Missing at least one request fields: {", ".join(*args)}'


class InvalidUsernameError(ValueError):
    """Exception raised for an invalid username."""
    def __init__(self, name, *args):
        self.message = f'Username "{name}" is invalid'


class UpdateMatchScoreForFinishedMatchError(TennisScoreboardError):
    """Exception raised when trying to update the score in a completed match."""
    def __init__(self, *args):
        self.message = 'Attempt update match score for already finished match.'





