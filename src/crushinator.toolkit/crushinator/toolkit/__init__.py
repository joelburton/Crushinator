import logging

# configure package-wide logger, collects messages but does not output them anywhere
# tap into this logger to see what's going on

# python pre-2.7 compatibilty
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logger = logging.getLogger('crushinator.toolkit')
logger.setLevel(logging.DEBUG)
logger.addHandler(NullHandler())