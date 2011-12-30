# This uses Maya stuff
try:
    import maya
except ImportError:
    pass
else:
    from .attributes import *
    from .containers import *
    from .nodes import *
    from .items import Separator

# This should be importable to Nuke
from . import components


