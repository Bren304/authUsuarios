from config.connection import db
from sqlalchemy import relationship

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desctiption = db.Column(db.String(200), nullable=True)

    # Relación inversa (un rol puede tener muchos usuarios)
    users = relationship('User', back_populates='role')

    def __repr__(self):
        return f"<Role {self.name}>"
