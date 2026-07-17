"""
Holds the "current clinic" for the duration of a request/task using a
contextvar (safe across both sync WSGI and async ASGI execution, unlike
threading.local). Set by core.middleware.TenantMiddleware on every
request; read by core.managers.TenantManager to scope querysets.

Nothing here talks to the database — it's pure in-memory request state.
"""
import contextvars

_current_clinic_id = contextvars.ContextVar("current_clinic_id", default=None)


def set_current_clinic_id(clinic_id):
    return _current_clinic_id.set(clinic_id)


def get_current_clinic_id():
    return _current_clinic_id.get()


def clear_current_clinic_id():
    _current_clinic_id.set(None)
