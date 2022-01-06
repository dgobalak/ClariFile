

class NoKeywordsFoundException(Exception):
    """Exception for when no keywords are found in the content"""
    pass


class UnsupportedFileTypeException(Exception):
    """Exception for when the input file type is not supported"""
    pass
