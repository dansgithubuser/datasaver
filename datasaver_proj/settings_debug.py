from .settings import *

DEBUG=True
ALLOWED_HOSTS=['*']

del SECURE_HSTS_SECONDS
del SECURE_CONTENT_TYPE_NOSNIFF
del SECURE_BROWSER_XSS_FILTER
del SECURE_SSL_REDIRECT
del SESSION_COOKIE_SECURE
del CSRF_COOKIE_SECURE
del X_FRAME_OPTIONS
del SECURE_HSTS_INCLUDE_SUBDOMAINS
del SECURE_HSTS_PRELOAD
