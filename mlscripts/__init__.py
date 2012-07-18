__all__ = ('VERSION',)

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('mlscripts').version
except Exception, e:
    VERSION = 'unknown'
