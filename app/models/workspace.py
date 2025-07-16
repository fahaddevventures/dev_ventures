from app.extensions import db
from datetime import datetime, timezone
from sqlalchemy import event


class Workspace(db.Model):
    __tablename__ = 'workspaces'

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False, unique=True)  # e.g., "Frontend"
    description = db.Column(db.Text, nullable=True)
    
    invite_code = db.Column(db.String(50), unique=True, nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Workspace {self.id} - {self.name}>"
    
# Auto-generate invite_code if not provided
@event.listens_for(Workspace, 'before_insert')
def add_invite_code(mapper, connection, target):
    # local import here to avoid circular import
    from app.utils.invite_code import generate_unique_invite_code

    if not target.invite_code:
        target.invite_code = generate_unique_invite_code(target.name)
