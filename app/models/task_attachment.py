from app.extensions import db
from datetime import datetime, timezone



class TaskAttachment(db.Model):
    __tablename__ = 'task_attachments'

    id = db.Column(db.Integer, primary_key=True)
    
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(512), nullable=False)  # Path or storage URL (e.g., AWS S3, local)
    
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    task = db.relationship('Task', backref=db.backref('attachments', cascade='all, delete-orphan'))
    uploader = db.relationship('User', backref=db.backref('uploaded_attachments', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<TaskAttachment {self.id} - {self.file_name}>"