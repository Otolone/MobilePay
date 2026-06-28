"""Shared Flask extension instances.

Kept in their own module so blueprints can import them (e.g. for the
@limiter.limit decorator) without importing app.py and creating a cycle.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# No global default_limits on purpose: a blanket limit would also throttle
# the PawaPay webhooks and status-polling endpoints. Limits are applied
# explicitly on sensitive routes (e.g. auth) instead.
#
# The default in-memory store is fine for a single process. For a multi-worker
# / multi-instance deployment, configure a shared backend via
# storage_uri="redis://..." so limits are enforced across workers.
limiter = Limiter(key_func=get_remote_address)
