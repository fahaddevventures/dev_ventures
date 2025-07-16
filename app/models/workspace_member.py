from app.extensions import db
from datetime import datetime, timezone

class WorkspaceMember(db.Model):
    __tablename__ = 'workspace_members'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id'), primary_key=True)

    joined_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = db.relationship('User', backref=db.backref('workspace_memberships', cascade='all, delete-orphan'))
    workspace = db.relationship('Workspace', backref=db.backref('members', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<WorkspaceMember user_id={self.user_id}, workspace_id={self.workspace_id}>"

