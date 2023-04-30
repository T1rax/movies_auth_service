class RegistrationException(Exception):
    """
    In case user cannot be registered
    Usually when user already exists
    or incorrect data provided
    """

    pass


class LoginException(Exception):
    """
    In case user cannot be logged in
    Usually when there are no provided login in database
    or when incorrect data provided
    """

    pass


class OAuthException(Exception):
    """
    Usually raises when they try to login, using social account
    from not supported provider
    """

    pass


class UserIdException(Exception):
    """
    Icorrect userid
    """

    pass


class HistoryException(Exception):
    """
    Could not provide user's history
    """

    pass
