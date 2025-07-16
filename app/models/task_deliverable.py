from app.extensions import db


class TaskDeliverable(db.Model):
    __tablename__ = 'task_deliverables'

    id = db.Column(db.Integer, primary_key=True)

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    is_submitted = db.Column(db.Boolean, default=False, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False)

    task = db.relationship('Task', backref=db.backref('deliverables', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<TaskDeliverable {self.id} - {self.title}>"