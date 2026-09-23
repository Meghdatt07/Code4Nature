import os
from sqlalchemy import create_engine,String,Integer,Float,DateTime,Text,ForeignKey
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship,sessionmaker
DATABASE_URL=os.getenv("DATABASE_URL","sqlite:///./asterisk_climos.db")
connect_args={"check_same_thread":False} if DATABASE_URL.startswith("sqlite") else {}
engine=create_engine(DATABASE_URL,connect_args=connect_args,future=True)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False,future=True)
class Base(DeclarativeBase): pass
class Farm(Base):
    __tablename__="farms"; id:Mapped[int]=mapped_column(Integer,primary_key=True); name:Mapped[str]=mapped_column(String(200),default="Demo Farm"); owner_id:Mapped[int|None]=mapped_column(Integer,nullable=True); geometry_geojson:Mapped[str]=mapped_column(Text,nullable=False); latitude:Mapped[float]=mapped_column(Float); longitude:Mapped[float]=mapped_column(Float); area_hectares:Mapped[float]=mapped_column(Float); area_acres:Mapped[float]=mapped_column(Float); soil_type:Mapped[str]=mapped_column(String(50),default="Loam"); season:Mapped[str]=mapped_column(String(30),default="Kharif"); crop_type:Mapped[str]=mapped_column(String(50),default="Rice"); created_at:Mapped[object]=mapped_column(DateTime,nullable=False); updated_at:Mapped[object]=mapped_column(DateTime,nullable=False); simulations=relationship("Simulation",back_populates="farm",cascade="all, delete-orphan")
class FarmMeasurement(Base):
    __tablename__="farm_measurements"; id:Mapped[int]=mapped_column(Integer,primary_key=True); farm_id:Mapped[int]=mapped_column(ForeignKey("farms.id"),index=True); measurement_date:Mapped[object]=mapped_column(DateTime,nullable=False); water_level:Mapped[float|None]=mapped_column(Float); soil_moisture:Mapped[float|None]=mapped_column(Float); rainfall:Mapped[float|None]=mapped_column(Float); irrigation_volume:Mapped[float|None]=mapped_column(Float); methane_measurement:Mapped[float|None]=mapped_column(Float); measurement_source:Mapped[str]=mapped_column(String(100),default="synthetic_demo")
class Simulation(Base):
    __tablename__="simulations"; id:Mapped[int]=mapped_column(Integer,primary_key=True); farm_id:Mapped[int]=mapped_column(ForeignKey("farms.id"),index=True); model_version:Mapped[str]=mapped_column(String(50)); baseline_water:Mapped[float]=mapped_column(Float); project_water:Mapped[float]=mapped_column(Float); baseline_emission:Mapped[float]=mapped_column(Float); project_emission:Mapped[float]=mapped_column(Float); emission_reduction:Mapped[float]=mapped_column(Float); water_saved:Mapped[float]=mapped_column(Float); carbon_price:Mapped[float]=mapped_column(Float); potential_credits:Mapped[float]=mapped_column(Float); gross_value:Mapped[float]=mapped_column(Float); farmer_share:Mapped[float]=mapped_column(Float); company_share:Mapped[float]=mapped_column(Float); input_json:Mapped[str]=mapped_column(Text); output_json:Mapped[str]=mapped_column(Text); created_at:Mapped[object]=mapped_column(DateTime,nullable=False); farm=relationship("Farm",back_populates="simulations")
class Scenario(Base):
    __tablename__="scenarios"; id:Mapped[int]=mapped_column(Integer,primary_key=True); name:Mapped[str]=mapped_column(String(50),unique=True); description:Mapped[str]=mapped_column(Text); baseline_emission:Mapped[float]=mapped_column(Float); project_emission:Mapped[float]=mapped_column(Float); baseline_water:Mapped[float]=mapped_column(Float); project_water:Mapped[float]=mapped_column(Float); carbon_price:Mapped[float]=mapped_column(Float); farmer_share:Mapped[float]=mapped_column(Float); company_share:Mapped[float]=mapped_column(Float)
class MRVRecord(Base):
    __tablename__="mrv_records"; id:Mapped[int]=mapped_column(Integer,primary_key=True); farm_id:Mapped[int]=mapped_column(ForeignKey("farms.id"),index=True); measurement_type:Mapped[str]=mapped_column(String(100)); value:Mapped[float|None]=mapped_column(Float); unit:Mapped[str]=mapped_column(String(50)); source:Mapped[str]=mapped_column(String(100)); timestamp:Mapped[object]=mapped_column(DateTime,nullable=False); verification_status:Mapped[str]=mapped_column(String(50),default="DEMO DATA")
class User(Base):
    __tablename__="users"; id:Mapped[int]=mapped_column(Integer,primary_key=True); name:Mapped[str]=mapped_column(String(100)); email:Mapped[str]=mapped_column(String(200),unique=True); role:Mapped[str]=mapped_column(String(50),default="farmer"); created_at:Mapped[object]=mapped_column(DateTime,nullable=False)
def init_db(): Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()