from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,Text
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.db.database import Base

class Farm(Base):
    __tablename__='farms'
    id=Column(Integer,primary_key=True)
    name=Column(String(160),nullable=False)
    owner_id=Column(Integer,nullable=True)
    geometry=Column(Geometry('POLYGON',srid=4326),nullable=True)
    latitude=Column(Float); longitude=Column(Float); area_hectares=Column(Float); area_acres=Column(Float)
    soil_type=Column(String(80)); season=Column(String(40)); crop_type=Column(String(80)); created_at=Column(DateTime(timezone=True),server_default=func.now()); updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

class FarmMeasurement(Base):
    __tablename__='farm_measurements'
    id=Column(Integer,primary_key=True); farm_id=Column(Integer,ForeignKey('farms.id')); measurement_date=Column(DateTime(timezone=True),server_default=func.now()); water_level=Column(Float); soil_moisture=Column(Float); rainfall=Column(Float); irrigation_volume=Column(Float); methane_measurement=Column(Float); measurement_source=Column(String(80))

class Simulation(Base):
    __tablename__='simulations'
    id=Column(Integer,primary_key=True); farm_id=Column(Integer,nullable=True); model_version=Column(String(40)); baseline_water=Column(Float); project_water=Column(Float); baseline_emission=Column(Float); project_emission=Column(Float); emission_reduction=Column(Float); water_saved=Column(Float); carbon_price=Column(Float); potential_credits=Column(Float); gross_value=Column(Float); farmer_share=Column(Float); company_share=Column(Float); created_at=Column(DateTime(timezone=True),server_default=func.now())

class Scenario(Base):
    __tablename__='scenarios'
    id=Column(Integer,primary_key=True); name=Column(String(80)); description=Column(Text); baseline_emission=Column(Float); project_emission=Column(Float); baseline_water=Column(Float); project_water=Column(Float); carbon_price=Column(Float); farmer_share=Column(Float); company_share=Column(Float)

class MRVRecord(Base):
    __tablename__='mrv_records'
    id=Column(Integer,primary_key=True); farm_id=Column(Integer); measurement_type=Column(String(80)); value=Column(Float); unit=Column(String(40)); source=Column(String(120)); timestamp=Column(DateTime(timezone=True),server_default=func.now()); verification_status=Column(String(50))

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True); name=Column(String(120)); email=Column(String(200),unique=True); role=Column(String(40)); created_at=Column(DateTime(timezone=True),server_default=func.now())
