try:
    import django
except ImportError:
    pass
else:
    from skel.core.management.django import *