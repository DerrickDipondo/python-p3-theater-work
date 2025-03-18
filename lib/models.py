from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean, sessionmaker
from sqlalchemy.orm import relationship, backref, declarative_base, Session
from sqlalchemy import create_engine, Role

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

engine = create_engine('sqlite:///theater.db')
Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String(255), nullable=False)

    auditions = relationship('Audition', backref='role', lazy='dynamic')

    def actors(self):
        """Return a list of actors for this role using SQLAlchemy query."""
        return [a.actor for a in self.auditions.all()]

    def locations(self):
        """Return a list of audition locations using SQLAlchemy query."""
        return [a.location for a in self.auditions.all()]

    def lead(self):
        """Return the first hired actor for this role, if any."""
        return self.auditions.filter_by(hired=True).order_by(Audition.id).first() or "no actor has been hired for this role"

    def understudy(self):
        """Return the second hired actor if available, otherwise return a default message."""
        hired_auditions = self.auditions.filter_by(hired=True).order_by(Audition.id).limit(2).all()
        return hired_auditions[1] if len(hired_auditions) > 1 else "no actor has been hired for understudy for this role"

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    phone = Column(String(20)) 
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    def mark_as_hired(self, session: Session):
        """Mark the audition as hired and commit changes."""
        self.hired = True
        session.add(self)
        session.commit()

Session = sessionmaker(bind=engine)
session = Session()

roles = session.query(Role).all()
if roles:
    for role in roles:
        print(role.id, role.character_name)
else:
    print("No roles found in the database.")