import json,os
from datetime import datetime,timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.database import init_db,SessionLocal,Farm,Scenario,MRVRecord
from .api import farms,simulations,carbon,scenarios,mrv,reports

app=FastAPI(title="Asterisk Climos API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=os.getenv("CORS_ORIGINS","http://localhost:3000").split(","),allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(farms.router); app.include_router(simulations.router); app.include_router(carbon.router); app.include_router(scenarios.router); app.include_router(mrv.router); app.include_router(reports.router)

@app.on_event("startup")
def startup():
    init_db(); seed_defaults()

@app.get("/health")
def health(): return {"status":"ok","mode":"prototype","model_version":"demo-v1.0"}

def seed_defaults():
    db=SessionLocal()
    try:
        if db.query(Scenario).count()==0:
            db.add_all([
                Scenario(name="CONSERVATIVE",description="Lower illustrative assumptions.",baseline_emission=6.0,project_emission=4.2,baseline_water=4960000,project_water=3650000,carbon_price=15,farmer_share=60,company_share=40),
                Scenario(name="BASE DEMO",description="Primary demonstration assumptions.",baseline_emission=6.0,project_emission=3.5,baseline_water=4960000,project_water=3140000,carbon_price=20,farmer_share=60,company_share=40),
                Scenario(name="CUSTOM",description="User-defined simulation inputs.",baseline_emission=6.0,project_emission=3.5,baseline_water=4960000,project_water=3140000,carbon_price=20,farmer_share=60,company_share=40)])
        if db.query(Farm).count()==0:
            demo=[("IN-001","Telangana",17.27033,79.29268,6.57,"Silt Loam"),("IN-002","West Bengal",23.25247,87.72022,1.39,"Sandy Loam"),("IN-003","Punjab",30.70111,75.78996,8.16,"Sandy Loam"),("IN-004","Haryana",29.71602,77.15470,3.01,"Sandy Loam"),("IN-005","Odisha",20.29606,85.82454,4.50,"Loam"),("IN-006","Telangana",17.38500,78.48670,10.00,"Loam")]
            now=datetime.now(timezone.utc).replace(tzinfo=None)
            for farm_id,state,lat,lon,area,soil in demo:
                dlat=(area**0.5)/111/2; dlon=(area**0.5)/(111*max(.2,abs(__import__("math").cos(__import__("math").radians(lat)))))/2
                geom={"type":"Polygon","coordinates":[[[lon-dlon,lat-dlat],[lon+dlon,lat-dlat],[lon+dlon,lat+dlat],[lon-dlon,lat+dlat],[lon-dlon,lat-dlat]]]}
                db.add(Farm(name=farm_id,geometry_geojson=json.dumps(geom),latitude=lat,longitude=lon,area_hectares=area,area_acres=area*2.47105381,soil_type=soil,season="Kharif",crop_type="Rice",created_at=now,updated_at=now))
        db.commit()
        if db.query(MRVRecord).count()==0:
            now=datetime.now(timezone.utc).replace(tzinfo=None)
            for farm in db.query(Farm).limit(10).all():
                for typ,val,unit in [("water_level",8,"cm"),("soil_moisture",31,"%"),("irrigation_volume",120000,"L"),("methane_measurement",None,"ppm")]:
                    db.add(MRVRecord(farm_id=farm.id,measurement_type=typ,value=val,unit=unit,source="synthetic_demo",timestamp=now,verification_status="DEMO DATA"))
            db.commit()
    finally:
        db.close()
