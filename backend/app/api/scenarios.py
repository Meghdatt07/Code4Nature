from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ._deps import get_db
from ..models.database import Scenario
from ..schemas.simulation import ScenarioCalculate
from ..services.simulation_service import calculate_simulation
router=APIRouter(prefix="/api/scenarios",tags=["scenarios"])
@router.get("")
def scenarios(db:Session=Depends(get_db)):
    rows=db.query(Scenario).order_by(Scenario.id).all()
    return [{"id":r.id,"name":r.name,"description":r.description,"baseline_emission":r.baseline_emission,"project_emission":r.project_emission,"baseline_water":r.baseline_water,"project_water":r.project_water,"carbon_price":r.carbon_price,"farmer_share":r.farmer_share,"company_share":r.company_share} for r in rows]
@router.post("/calculate")
def calculate(payload:ScenarioCalculate): return calculate_simulation(area_ha=payload.area_hectares,soil_type=payload.soil_type,season=payload.season,crop_duration_days=payload.crop_duration_days,management_type=payload.management_type,baseline_water_liters=payload.baseline_water,rainfall_assumption_mm=payload.rainfall_assumption_mm,baseline_emission_tco2e_per_ha=payload.baseline_emission,reduction_percent=payload.reduction_percent,carbon_price_usd=payload.carbon_price,farmer_share=payload.farmer_share,company_share=payload.company_share,fx_rate=payload.fx_rate)
@router.get("/dashboard/admin")
def admin_dashboard():
    import csv
    from pathlib import Path
    path=Path(__file__).resolve().parents[2]/"data"/"synthetic_farms.csv"
    with path.open() as f: rows=list(csv.DictReader(f))
    water_saved=sum(float(r["baseline_water_liters"])-float(r["project_water_liters"]) for r in rows); reduction=sum(float(r["emission_reduction_tco2e"]) for r in rows); credits=sum(float(r["potential_credits"]) for r in rows); gross=sum(float(r["gross_value_usd"]) for r in rows)
    return {"total_farms":len(rows),"total_hectares":sum(float(r["area_hectares"]) for r in rows),"simulated_water_saved_liters":water_saved,"simulated_reduction_tco2e":reduction,"potential_credits":credits,"gross_value_usd":gross,"farmer_revenue_usd":gross*.60,"company_revenue_usd":gross*.40,"data_source":"synthetic_demo"}