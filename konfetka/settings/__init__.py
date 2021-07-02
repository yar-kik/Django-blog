from .base import *

if os.environ.get("DJANGO_ENV", "development") == "production":
    from .prod import *
else:
    from .dev import *
