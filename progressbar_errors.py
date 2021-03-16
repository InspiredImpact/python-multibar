class MissingArgument(Exception):
    """
    Raised when one of the args is missing
    """
    pass

class BadArgument(Exception):
    """
    Raised when specified bad arg
    """
    pass

class ProgressError(Exception):
    """
    Raised when [progress_now] > [needed_progress]
    """
    pass

class TooLargeArgument(Exception):
    """
    Raised when embed position idx > 25
    """
    pass

class TooManyFields(Exception):
    """
    Raised when len(embed fields) + field with progressbar > 25
    """
    pass

class BadEmbed(BadArgument):
    """
    Raised when embed != discord.Embed()
    """
    pass

class BadType(BadArgument):
    """
    Raised when type not in [post / get]
    """
    pass
