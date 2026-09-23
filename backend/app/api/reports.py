import json
from io import BytesIO
from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from ._deps import get_db
from ..models.database import Simulation,Farm
router=APIRouter(prefix="/api/reports",tags=["reports"])
@router.get("/simulations/{simulation_id}.pdf")
def report(simulation_id:int,db:Session=Depends(get_db)):
    sim=db.get(Simulation,simulation_id)
    if not sim: raise HTTPException(404,"Simulation not found")
    farm=db.get(Farm,sim.farm_id)
    if not farm: raise HTTPException(404,"Farm not found")
    result=json.loads(sim.output_json); buf=BytesIO(); c=canvas.Canvas(buf,pagesize=A4); W,H=A4
    c.setTitle("Asterisk Climos Prototype Simulation Report"); c.setFont("Helvetica-Bold",20); c.drawString(42,H-55,"ASTERISK CLIMOS"); c.setFont("Helvetica",10); c.drawString(42,H-72,"Measure. Optimize. Reduce. Value."); c.setFont("Helvetica-Bold",12); c.drawString(42,H-105,"Prototype Simulation - Not a Carbon Credit Certificate")
    y=H-150
    lines=[("Farm",farm.name),("Area",str(round(farm.area_hectares,2))+" ha"),("Baseline water",format(result["baseline_water_liters"],",.0f")+" L"),("Project water",format(result["project_water_liters"],",.0f")+" L"),("Estimated reduction",format(result["emission_reduction_tco2e"],".2f")+" tCO2e"),("Potential credits",format(result["potential_credits"],".2f")),("Gross value","$"+format(result["gross_value_usd"],",.2f")+" / INR "+format(result["gross_value_inr"],",.2f")),("Farmer share","$"+format(result["farmer_revenue_usd"],",.2f")),("Company share","$"+format(result["company_revenue_usd"],",.2f"))]
    for k,v in lines:
        c.drawString(42,y,k+": "+v); y-=20
    c.setFont("Helvetica-Bold",10); c.drawString(42,50,"Illustrative prototype output; not a certified carbon-credit certificate.")
    c.save(); buf.seek(0)
    return StreamingResponse(buf,media_type="application/pdf",headers={"Content-Disposition":"attachment; filename=asterisk_climos_simulation_"+str(simulation_id)+".pdf"})