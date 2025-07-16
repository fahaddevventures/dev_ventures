from app.extensions import db

class UserSkill(db.Model):
    __tablename__ = 'user_skills'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)

    proficiency = db.Column(db.String(50), nullable=True)  # Optional: e.g., 'beginner', 'intermediate', 'expert'

    user = db.relationship('User', backref=db.backref('user_skills', cascade='all, delete-orphan'))
    skill = db.relationship('Skill', backref=db.backref('user_skills', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<UserSkill UserID={self.user_id} SkillID={self.skill_id} Proficiency={self.proficiency}>"