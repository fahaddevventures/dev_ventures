from app.extensions import db
from datetime import datetime, timezone



class ProjectAttachment(db.Model):
    __tablename__ = 'project_attachments'

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(512), nullable=False)  # URL or file path

    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    project = db.relationship('Project', backref=db.backref('attachments', cascade='all, delete-orphan'))
    uploader = db.relationship('User', backref=db.backref('uploaded_project_attachments', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<ProjectAttachment {self.id} - {self.file_name}>"