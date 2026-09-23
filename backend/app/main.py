import os, io, json, csv, random, math
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from .services.simulation import run_simulation, MODEL_VERSION
from .db.database import engine, Base
try:
    from .models.database_models import Simulation as SimulationRow
except Exception:
    SimulationRow=None

if engine is not None:
    try: Base.metadata.create_all(bind=engine)
    except Exception: pass

app=FastAPI(title='CarbonAWD API', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
FX=float(os.getenv('DEMO_FX_USD_INR','83'))

class FarmIn(BaseModel):
    name:str='Demo Farm'; geometry:dict|None=None; latitude:float=17.385; longitude:float=78.4867
    soil_type:str='Loam'; crop_type:str='Rice'; season:str='Kharif'; area_hectares:float=10
class SimIn(BaseModel):
    farm_id:str='demo-10ha'; farm_area_ha:float=10; soil_type:str='Loam'; season:str='Kharif'; crop_days:int=120
    baseline_water_liters_per_acre:float=4_960_000; water_reduction_pct:float=36.7
    baseline_emission_tco2e_ha:float=6.0; emission_reduction_pct:float=41.6666667
    carbon_price_usd:float=20; farmer_share:float=60; company_share:float=40

@app.get('/health')
def health(): return {'status':'ok','mode':'prototype','model_version':MODEL_VERSION}

@app.post('/api/farms')
def create_farm(f:FarmIn):
    if f.area_hectares<=0: raise HTTPException(400,'Area must be greater than zero')
    return {'id':'demo-'+f.name.lower().replace(' ','-'), **f.model_dump(), 'area_acres':f.area_hectares*2.47105381, 'data_source':'user_input'}

@app.get('/api/farms')
def farms(): return {'items':generate_farms(100)}

@app.post('/api/simulations')
def simulation(s:SimIn):
    try:
        result=run_simulation(**s.model_dump(exclude={'farm_id'}), fx=FX)
        if engine is not None and SimulationRow is not None:
            try:
                from .db.database import SessionLocal
                db=SessionLocal()
                db.add(SimulationRow(farm_id=None, model_version=MODEL_VERSION, baseline_water=result['baseline_water_liters_per_acre'], project_water=result['project_water_liters_per_acre'], baseline_emission=result['baseline_emission_total_tco2e'], project_emission=result['project_emission_total_tco2e'], emission_reduction=result['emission_reduction_tco2e'], water_saved=result['total_water_saved_liters'], carbon_price=result['carbon_price_usd'], potential_credits=result['potential_credits'], gross_value=result['gross_value_usd'], farmer_share=result['farmer_share_percent'], company_share=result['company_share_percent']))
                db.commit(); db.close()
            except Exception: pass
        return result
    except ValueError as e:
        raise HTTPException(400,str(e))

@app.post('/api/scenarios/calculate')
def scenarios(s:SimIn): return simulation(s)

@app.get('/api/mrv/{farm_id}')
def mrv(farm_id:str):
    return {'farm_id':farm_id,'status':'DEMO DATA','records':[
        {'measurement_type':'water_level','value':2.0,'unit':'cm','source':'synthetic_demo','verification_status':'demo'},
        {'measurement_type':'soil_moisture','value':31,'unit':'%','source':'synthetic_demo','verification_status':'demo'},
        {'measurement_type':'irrigation','value':1,'unit':'event','source':'synthetic_demo','verification_status':'demo'}]}

@app.get('/api/scenarios')
def scenario_list():
    return {'items':[
      {'name':'Conservative','water_reduction_pct':20,'emission_reduction_pct':25,'carbon_price_usd':15,'farmer_share':60},
      {'name':'Base Demo','water_reduction_pct':36.7,'emission_reduction_pct':41.6666667,'carbon_price_usd':20,'farmer_share':60},
      {'name':'Custom','water_reduction_pct':30,'emission_reduction_pct':30,'carbon_price_usd':25,'farmer_share':60}]}

def generate_farms(n):
    random.seed(42); out=[]
    states=[('Telangana',17.5,79.0),('Andhra Pradesh',16.5,80.6),('West Bengal',23.0,87.8),('Odisha',20.3,85.8),('Punjab',30.9,75.8),('Chhattisgarh',21.3,81.9)]
    soils=['Clay','Loam','Sandy Loam','Silt Loam']; seasons=['Kharif','Rabi']
    for i in range(n):
        state,lat,lon=random.choice(states); area=round(random.uniform(.5,10),2); base=round(random.uniform(3,8),2); red=round(random.uniform(15,55),2); proj=round(base*(1-red/100),2); price=random.choice([15,20,25]); reduction=round(area*(base-proj),2)
        out.append({'farm_id':f'DEMO-{i+1:03}','state':state,'district':'Synthetic','latitude':round(lat+random.uniform(-.6,.6),5),'longitude':round(lon+random.uniform(-.6,.6),5),'area_hectares':area,'area_acres':round(area*2.47105,2),'soil_type':random.choice(soils),'season':random.choice(seasons),'crop_duration':random.choice([100,120,135,150]),'baseline_water_liters':round(area*2.47105*4_960_000),'project_water_liters':round(area*2.47105*4_960_000*(1-random.uniform(.2,.4))),'baseline_emission_tco2e':round(area*base,2),'project_emission_tco2e':round(area*proj,2),'water_saving_percent':round(random.uniform(20,40),2),'emission_reduction_tco2e':reduction,'carbon_price_usd':price,'potential_credits':reduction,'gross_value_usd':round(reduction*price,2),'farmer_share':60,'company_share':40,'data_source':'synthetic_demo'})
    return out

@app.get('/api/export/pdf')
def pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    result=run_simulation(10,fx=FX)
    b=io.BytesIO(); c=canvas.Canvas(b,pagesize=A4); w,h=A4
    y=h-55; c.setFont('Helvetica-Bold',20); c.drawString(45,y,'CARBONAWD'); y-=28
    c.setFont('Helvetica',11); c.drawString(45,y,'Prototype Simulation — Not a Carbon Credit Certificate'); y-=28
    for k,v in [('Farm area (ha)',result['farm_area_ha']),('Baseline emissions (tCO2e)',result['baseline_emission_total_tco2e']),('Project emissions (tCO2e)',result['project_emission_total_tco2e']),('Estimated reduction (tCO2e)',result['emission_reduction_tco2e']),('Potential credits',result['potential_credits']),('Carbon price (USD/tCO2e)',result['carbon_price_usd']),('Gross value (USD)',result['gross_value_usd']),('Farmer share (USD)',result['farmer_revenue_usd']),('Company share (USD)',result['company_revenue_usd'])]:
        c.drawString(55,y,f'{k}: {v}'); y-=19
    y-=10; c.setFont('Helvetica-Bold',10); c.drawString(45,y,'Scientific / data disclaimer'); y-=15; c.setFont('Helvetica',8)
    text='Calculated methane reductions, water savings, carbon-credit quantities and financial outcomes are illustrative unless explicitly identified as measured or published values. Actual carbon-credit eligibility and issuance require applicable methodologies, additionality assessment, MRV, validation, verification, registry requirements and project-specific evidence.'
    for line in [text[i:i+105] for i in range(0,len(text),105)]: c.drawString(45,y,line); y-=12
    c.save(); b.seek(0); return StreamingResponse(b,media_type='application/pdf',headers={'Content-Disposition':'attachment; filename=carbonawd-demo-report.pdf'})
