from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


# Define the data model for the database
class DashboardData(Base):
    __tablename__ = 'dashboard_data'
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String)
    pickup = Column(String)
    age = Column(String)
    origin = Column(String)
    destination = Column(String, nullable=True)
    weight = Column(String)
    distance = Column(String)
    price = Column(String)
    company = Column(String)
    phone = Column(String)

class CompanyData(Base):
    __tablename__ = 'company_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String, index=True)  # No primary key
    value = Column(Integer)

class TransportData(Base):
    __tablename__ = 'transport_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    pickup = Column(String, nullable=False)
    destination = Column(String, nullable=True)
    date = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    distance = Column(String, nullable=False)
    type = Column(String, nullable=False)