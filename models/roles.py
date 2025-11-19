from config.connection import db
from sqlalchemy.orm import relationship

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    # Relación inversa
    users = relationship('User', back_populates='role')

    def __repr__(self):
        return f"<Role {self.name}>"
    
    @classmethod
    def create_default_roles(cls):
        """Crea los roles por defecto si no existen"""
        default_roles = [
            {'name': 'user', 'description': 'Usuario normal'},
            {'name': 'admin', 'description': 'Administrador'}
        ]
        
        for role_data in default_roles:
            existing_role = cls.query.filter_by(name=role_data['name']).first()
            if not existing_role:
                new_role = cls(**role_data)
                db.session.add(new_role)
                print(f"Rol creado: {role_data['name']}")
        
        db.session.commit()