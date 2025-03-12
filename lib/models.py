from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Boolean

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

engine = create_engine('sqlite:///theater.db')

Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__= 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String(255), nullable=False)

    auditions = relationship('Audition', backref='role', lazy='dynamic')

    def actors(self):
        return[audition.actor for audition in self.auditions]
    
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        hired = [a for a in self.auditions if a.hired]
        return hired[0] if hired else "no one has been hired for this role"
    def understudy(self):
        hired = [a for a in self.auditions if a.hired]
        return hired[1] if len(hired) > 1 else "no one has been hired for understudy in this role"
    
class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    def call_back(self):
        self.hired = True
        


