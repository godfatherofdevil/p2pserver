class BadMessage(Exception):
    """
    raised when unexpected payload is received by any of the endpoints
    """
    pass


class OutOfOrderOperation(Exception):
    """
    raised when host tries to poll before registering any game session
    """