from app.extensions import db
from datetime import datetime, timezone
from app.enums import ProfileStatusEnum



class UpworkProfile(db.Model):
    __tablename__ = 'upwork_profiles'

    id = db.Column(db.Integer, primary_key=True)

    profile_name = db.Column(db.String(100), nullable=False)
    profile_url = db.Column(db.String(255), nullable=False)
    
    contact = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    upwork_password = db.Column(db.String(255), nullable=False)  # hashed or encrypted

    connects_available = db.Column(db.Integer, default=0, nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=True)

    status = db.Column(db.Enum(ProfileStatusEnum), default=ProfileStatusEnum.active, nullable=False)

    def __repr__(self):
        return f"<UpworkProfile {self.id} - {self.profile_name}>"