import json
from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ._deps import get_db
from ..models.database import Farm,Simulation
from ..schemas.simulation import SimulationCreate
from ..services.simulation_service import calculate_simulation
router=APIRouter(prefix="/api/simulations",tags=["simulations"])
def make_result(farm,payload):
    reduction=payload.reduction_percent
    if payload.project_emission is not None and payload.baseline_emission>0: reduction=(1-payload.project_emission/payload.baseline_emission)*100
    result=calculate_simulation(area_ha=farm.area_hectares,soil_type=payload.soil_type,season=payload.season,crop_duration_days=payload.crop_duration_days,management_type=payload.management_type,baseline_water_liters=payload.baseline_water,rainfall_assumption_mm=payload.rainfall_assumption_mm,baseline_emission_tco2e_per_ha=payload.baseline_emission,reduction_percent=reduction,carbon_price_usd=payload.carbon_price,farmer_share=payload.farmer_share,company_share=payload.company_share,fx_rate=payload.fx_rate)
    if payload.project_water is not None:
        result["project_water_liters"]=round(payload.project_water,2); result["water_saved_liters"]=round(max(0,payload.baseline_water-payload.project_water),2); result["water_saving_percent"]=round(result["water_saved_liters"]/payload.baseline_water*100 if payload.baseline_water else 0,2)
    return result
@router.post("")
def create_simulation(payload:SimulationCreate,db:Session=Depends(get_db)):
    farm=db.get(Farm,payload.farm_id)
    if not farm: raise HTTPException(404,"Farm not found")
    try: result=make_result(farm,payload)
    except ValueError as exc: raise HTTPException(400,str(exc))
    now=datetime.now(timezone.utc).replace(tzinfo=None)
    sim=Simulation(farm_id=farm.id,model_version=result["model_version"],baseline_water=result["baseline_water_liters"],project_water=result["project_water_liters"],baseline_emission=result["baseline_emission_total_tco2e"],project_emission=result["project_emission_total_tco2e"],emission_reduction=result["emission_reduction_tco2e"],water_saved=result["water_saved_liters"],carbon_price=result["carbon_price_usd"],potential_credits=result["potential_credits"],gross_value=result["gross_value_usd"],farmer_share=payload.farmer_share,company_share=payload.company_share,input_json=payload.model_dump_json(),output_json=json.dumps(result),created_at=now)
    db.add(sim); db.commit(); db.refresh(sim)
    return {"id":sim.id,"farm_id":farm.id,**result}
@router.get("/{simulation_id}")
def get_simulation(simulation_id:int,db:Session=Depends(get_db)):
    sim=db.get(Simulation,simulation_id)
    if not sim: raise HTTPException(404,"Simulation not found")
    return {"id":sim.id,"farm_id":sim.farm_id,**json.loads(sim.output_json)}