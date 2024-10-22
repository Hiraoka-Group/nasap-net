"""
**********
Exceptions
**********

Base exceptions and errors for RECSA.
"""

__all__ = [
    'RecsaException',
    'RecsaFileExistsError',
    'RecsaNotImplementedError',
    'RecsaParsingError',
    'RecsaRuntimeError',
    'RecsaTypeError',
    'RecsaValueError',
]


class RecsaException(Exception):
    """Base exception for the RECSA package."""
    pass


class RecsaTypeError(RecsaException):
    pass


class RecsaValueError(RecsaException):
    pass


class RecsaParsingError(RecsaException):
	"""Base class for parsing errors."""
	pass


class RecsaNotImplementedError(RecsaException):
    pass


class RecsaRuntimeError(RecsaException):
    pass


class RecsaFileExistsError(RecsaValueError):
    pass
