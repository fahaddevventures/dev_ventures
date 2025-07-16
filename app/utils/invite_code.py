import secrets
import string
import uuid
import re
from app.extensions import db
from app.models.workspace import Workspace

def slugify_name(name):
    """
    Returns first 5 uppercase characters from cleaned name (A-Z0-9)
    """
    slug = re.sub(r'[^A-Za-z0-9]', '', name)[:5].upper()
    return slug or "WS"

def generate_unique_invite_code(name, length=5, max_attempts=10):
    prefix = slugify_name(name)
    charset = string.ascii_uppercase + string.digits

    for _ in range(max_attempts):
        suffix = ''.join(secrets.choice(charset) for _ in range(length))
        code = f"{prefix}-{suffix}"
        exists = db.session.query(Workspace.id).filter_by(invite_code=code).first()
        if not exists:
            return code

    # Fallback to UUID
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"
.